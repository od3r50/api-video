from flask import Blueprint, request, jsonify, send_file
from app.video.controller import (
    start_render_job,
    get_job_status,
    get_job_result_path
)
from app.auth.decorators import token_required

bp = Blueprint("video", __name__)

@bp.route("/render", methods=["POST"])
@token_required
def render_video(current_user):
    body = request.json
    job_id = start_render_job(
        current_user,
        template_id=body["template_id"],
        modifications=body.get("modifications", {})
    )
    return jsonify({"job_id": job_id}), 202

@bp.route("/render/status/<job_id>", methods=["GET"])
@token_required
def check_status(current_user, job_id):
    job = get_job_status(job_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404
    return jsonify(job)

@bp.route("/render/result/<job_id>", methods=["GET"])
@token_required
def get_result(current_user, job_id):
    path = get_job_result_path(job_id)
    if not path:
        return jsonify({"error": "Video not ready"}), 404
    return send_file(path, as_attachment=True)
