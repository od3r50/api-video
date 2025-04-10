# app/celery_worker.py
from celery import Celery
from flask import Flask
import os

def make_celery(app_name=__name__):
    return Celery(
        app_name,
        broker=os.getenv("CELERY_BROKER_URL"),
        backend=os.getenv("CELERY_RESULT_BACKEND"),
    )

celery = make_celery()
