from flask import Blueprint, request, jsonify, send_file
from moviepy.editor import *
import json, os
from services.file_utils import clean_temp_files
from services.video import render_worker
from threading import Thread
from config import VIDEO_DIR
from uuid import uuid4

from services.video import process_elements

bp = Blueprint("render", __name__)
jobs = {}

def load_template(template_id, modifications):
    path = f"templates/{template_id}.json"
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

@bp.route("/render", methods=["POST"])
def render_video():
    body = request.json
    job_id = uuid4().hex
    output_path = f"outputs/{job_id}"

    def run():
        temp_dirs = []
        try:
            data = load_template(body["template_id"], body.get("modifications", {}))
            final_clip, audio_clip, temp_dirs = process_elements(data)
            output_path = os.path.join(VIDEO_DIR, f"{job_id}.mp4")
            from services.video import render_clip_in_thread
            render_clip_in_thread(final_clip, audio_clip, output_path, fps=24, job_id=job_id, jobs_dict=jobs)
        except Exception as e:
            jobs[job_id] = {"status": "error", "message": str(e)}

        finally:
            for td in temp_dirs:
                clean_temp_files(td)

    jobs[job_id] = {"status": "processing"}
    t = Thread(target=run)
    t.start()

    return jsonify({"job_id": job_id}), 202

@bp.route("/render/status/<job_id>", methods=["GET"])
def check_status(job_id):
    job = jobs.get(job_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404
    return jsonify(job)

@bp.route("/render/result/<job_id>", methods=["GET"])
def get_result(job_id):
    job = jobs.get(job_id)
    if not job or job["status"] != "done":
        return jsonify({"error": "Video not ready"}), 404
    return send_file(job["path"], as_attachment=True)
