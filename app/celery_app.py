from celery import Celery
import os

def make_celery():
    return Celery(
        'clikode-video-render',
        broker=os.getenv("CELERY_BROKER_URL"),
        backend=os.getenv("CELERY_RESULT_BACKEND"),
        include=["app.video.tasks"]  # garante que tasks sejam carregadas
    )

celery = make_celery()
