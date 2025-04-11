from app.factory import create_app
# Importa a instância BASE de celery_app.py
from app.celery_app import celery

# Chama create_app() para configurar a instância 'celery' importada acima
# A instância 'app' retornada não é usada diretamente aqui,
# mas a chamada configura o 'celery' importado.
app = create_app()

# Comando para iniciar o worker (a partir da raiz /app):
# celery -A celery_worker.celery worker --loglevel=INFO