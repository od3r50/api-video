import os
from app.celery_app import celery

from app.config import VIDEO_DIR
from app.video.utils import process_elements, load_template

@celery.task(bind=True, name='app.video.tasks.render_video_task')
def render_video_task(self, template_id, modifications):   
    output = os.path.join(VIDEO_DIR, f"{self.request.id}.mp4")

    try:
        data = load_template(template_id, modifications)
        clip, audio_clip, temp_dirs = process_elements(data)

        final_clip = clip.set_audio(audio_clip) if audio_clip else clip
        final_clip.write_videofile(output, fps=24)

    except Exception as e:
            print({"status": "error", "message": str(e)})
    
    return {
        "status": "completed",
        "output_path": f"/app/output/{self.request.id}_video.mp4"
    }



