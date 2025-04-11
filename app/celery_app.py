from celery import Celery
import os
from flask import Flask

# Instância BASE do Celery
celery = Celery(
    __name__, # Ou 'app' ou o nome do seu módulo principal
    broker=os.getenv("CELERY_BROKER_URL", 'redis://localhost:6379/0'),
    backend=os.getenv("CELERY_RESULT_BACKEND", 'redis://localhost:6379/0'),
    include=["app.video.tasks"] # Suas tasks
)

# Função para configurar a instância com a app Flask
def update_celery_config(app: Flask, celery_instance: Celery):
    celery_instance.conf.update(app.config)

    class ContextTask(celery_instance.Task):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_instance.Task = ContextTask
    return celery_instance