from flask import Flask
from app.config import Config
from app.extensions import db, migrate
from app.video.routes import bp as video_bp
from app.auth.routes import bp as auth_bp
# Remova imports não utilizados de models aqui se não forem necessários na factory
# from app.models.user import User
# from app.models.job import Job

# Importa de celery_app.py!
from app.celery_app import celery, update_celery_config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(video_bp, url_prefix="/video")

    # Configura a instância celery importada
    update_celery_config(app, celery)

    return app