from flask import Flask
from app.config import Config
from app.extensions import db, migrate
from app.video.routes import bp as video_bp
from app.auth.routes import bp as auth_bp
from app.models.user import User
from app.models.job import Job


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(video_bp, url_prefix="/video")

    return app
