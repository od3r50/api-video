from datetime import datetime, timezone
import os

from flask import current_app
from app.celery_app import celery

from app.config import VIDEO_DIR
from app.core import s3_service
from app.video.utils import process_elements, load_template
from app.models.job import Job
from app.extensions import db
from app.video.services import get_job_by_id

@celery.task(bind=True, name='app.video.tasks.render_video_task')
def render_video_task(self, template_id, modifications):
    job = get_job_by_id(self.request.id)
    
    s3_bucket_name = current_app.config.get('S3_BUCKET_NAME')
    output_object_name = f"{job.id}"
    url_minio = current_app.config.get("MINIO_URL_LOCAL")
    url_to_file = f"{url_minio}/{s3_bucket_name}/{output_object_name}"

    output = os.path.join(VIDEO_DIR, f"{self.request.id}.mp4")

    try:
        data = load_template(template_id, modifications)
        clip, audio_clip, temp_dirs = process_elements(data)

        final_clip = clip.set_audio(audio_clip) if audio_clip else clip
        final_clip.write_videofile(output, fps=24)

        upload_to_s3 = s3_service.upload_file_to_s3(output, s3_bucket_name, output_object_name)

        if not upload_to_s3:
             raise Exception("Falha no upload do video para o s3/minio")

        job.status = "completed"
        job.updated_at = datetime.now(timezone.utc)
        job.output_path = url_to_file
        db.session.commit()

    except Exception as e:
            job.status = "error"
            job.error_message = str(e)
            db.session.commit()
            print({"status": "error", "message": str(e)})
    
    return {
        "status": "completed",
        "output_path": url_to_file
    }
