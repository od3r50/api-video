from flask import Flask
from app.config import Config
from app.extensions import jwt
from app.auth.routes import auth_bp
from app.video.routes import video_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    jwt.init_app(app)

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(video_bp, url_prefix="/video")

    return app
