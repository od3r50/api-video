from flask import jsonify
from app.extensions import db
from app.models.job import Job

def get_job_by_id(id):

    job = Job.query.get(id)

    if not job:
        return jsonify({"error": "Resource not found"}), 404

    return job

def create_job(data):
    return data
