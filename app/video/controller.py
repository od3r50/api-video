import json, os
from uuid import uuid4
from threading import Thread

from app.video.services import process_elements, render_clip_in_thread

from app.services.file_utils import clean_temp_files
from app.config import VIDEO_DIR

jobs = {}

def load_template(template_id, modifications):
    path = f"app/templates/{template_id}.json"
    if not os.path.exists(path):
        raise FileNotFoundError("Template not found.")

    with open(path, "r") as f:
        template = json.load(f)

    for el in template["elements"]:
        name = el.get("name")
        if not name:
            continue
        for field, value in modifications.items():
            if field.startswith(name + "."):
                prop = field.split(".", 1)[1]
                el[prop] = value
    return template

def start_render_job(template_id, modifications):
    job_id = uuid4().hex
    jobs[job_id] = {"status": "processing"}

    output_path = os.path.join(VIDEO_DIR, f"{job_id}.mp4")

    def run():
        temp_dirs = []
        try:
            data = load_template(template_id, modifications)
            final_clip, audio_clip, temp_dirs = process_elements(data)
            render_clip_in_thread(final_clip, audio_clip, output_path, fps=24, job_id=job_id, jobs_dict=jobs)
        except Exception as e:
            jobs[job_id] = {"status": "error", "message": str(e)}
        finally:
            for td in temp_dirs:
                clean_temp_files(td)

    Thread(target=run).start()
    return job_id

def get_job_status(job_id):
    return jobs.get(job_id)

def get_job_result_path(job_id):
    job = jobs.get(job_id)
    if job and job["status"] == "done":
        return job["path"]
    return None
