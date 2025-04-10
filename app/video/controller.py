from app.video.tasks import render_video_task
from celery.result import AsyncResult
from app.celery_worker import celery
from app.models.job import Job
from app.extensions import db

def start_render_job(current_user, template_id, modifications):
    async_job = render_video_task.apply_async(args=[template_id, modifications])
    print(async_job, "---------->")
    job_data ={
        "id": async_job.id,
        "user_id": current_user.id,
        "template_id": template_id,
        "modifications": modifications,
        "status": "processing"
    }

    job = Job(**job_data)

    db.session.add(job)
    db.session.commit()

    return job.id

def get_job_status(job_id):
    result = AsyncResult(job_id, app=celery)
    return {
        "id": job_id,
        "state": result.state,
        "info": result.info if result.state == "SUCCESS" else None
    }

def get_job_result_path(job_id):
    result = AsyncResult(job_id, app=celery)
    if result.state == "SUCCESS":
        return result.info["output_path"]
    return None
