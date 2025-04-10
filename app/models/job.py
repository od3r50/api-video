from app.extensions import db
from datetime import datetime, timezone

class Job(db.Model):
    __tablename__ = "jobs"
    id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')
    output_path = db.Column(db.String, nullable=True)
    error_message = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    template_id = db.Column(db.String, nullable=False)
    modifications = db.Column(db.JSON, nullable=True)
