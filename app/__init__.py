from flask import Flask
from app.config import Config
from flask_migrate import Migrate
# from app.extensions import jwt
# from app.auth.routes import auth_bp
from app.extensions import db, migrate
from app.video.routes import bp as video_bp
from app.auth.routes import bp as auth_bp
from app.models.user import User


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    # jwt.init_app(app)

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(video_bp, url_prefix="/video")

    return app
