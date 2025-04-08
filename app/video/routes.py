from flask import Blueprint, request, jsonify, send_file
from app.video.controller import (
    start_render_job,
    get_job_status,
    get_job_result_path
)

video_bp = Blueprint("video", __name__)

@video_bp.route("/render", methods=["POST"])
def render_video():
    body = request.json
    job_id = start_render_job(
        template_id=body["template_id"],
        modifications=body.get("modifications", {})
    )
    return jsonify({"job_id": job_id}), 202

@video_bp.route("/render/status/<job_id>", methods=["GET"])
def check_status(job_id):
    job = get_job_status(job_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404
    return jsonify(job)

@video_bp.route("/render/result/<job_id>", methods=["GET"])
def get_result(job_id):
    path = get_job_result_path(job_id)
    if not path:
        return jsonify({"error": "Video not ready"}), 404
    return send_file(path, as_attachment=True)
