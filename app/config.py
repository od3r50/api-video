from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

# Diretório base do projeto (vai pegar até /app)
BASE_DIR = Path(__file__).resolve().parent.parent
VIDEO_DIR = BASE_DIR / "videos"
VIDEO_DIR.mkdir(parents=True, exist_ok=True)

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret")

    DB_USER = os.getenv("POSTGRES_USER", "postgres")
    DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
    DB_HOST = os.getenv("POSTGRES_HOST", "db")  # nome do serviço no docker-compose
    DB_PORT = os.getenv("POSTGRES_PORT", "5432")
    DB_NAME = os.getenv("POSTGRES_DB", "vapi")

    S3_ENDPOINT_URL = os.getenv('S3_ENDPOINT_URL')
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_KEY_ID = os.getenv('AWS_SECRET_KEY_ID') # <- Corrigido aqui, estava 'KEY_ID' duplicado no meu exemplo anterior, perdão.
    S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
    AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
    S3_USE_SSL = os.getenv('S3_USE_SSL', 'false').lower() == 'true'