from datetime import datetime, timezone
import os
from app.celery_app import celery

from app.config import VIDEO_DIR
from app.video.utils import process_elements, load_template
from app.models.job import Job
from app.extensions import db

@celery.task(bind=True, name='app.video.tasks.render_video_task')
def render_video_task(self, template_id, modifications):
    job = Job.query.get(self.request.id)

    output = os.path.join(VIDEO_DIR, f"{self.request.id}.mp4")

    try:
        data = load_template(template_id, modifications)
        clip, audio_clip, temp_dirs = process_elements(data)

        final_clip = clip.set_audio(audio_clip) if audio_clip else clip
        final_clip.write_videofile(output, fps=24)

        job.status = "completed"
        job.updated_at = datetime.now(timezone.utc)
        job.output_path = output
        db.session.commit()

    except Exception as e:
            job.status = "error"
            job.error_message = str(e)
            db.session.commit()
            print({"status": "error", "message": str(e)})
    
    return {
        "status": "completed",
        "output_path": output
    }
