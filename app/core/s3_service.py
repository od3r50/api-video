import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
import logging
from flask import current_app 

logger = logging.getLogger(__name__)

_s3_client = None 

def get_s3_client():
    global _s3_client
    if _s3_client:
        return _s3_client

    endpoint_url = current_app.config.get('S3_ENDPOINT_URL')
    access_key = current_app.config.get('AWS_ACCESS_KEY_ID')
    secret_key = current_app.config.get('AWS_SECRET_KEY_ID')
    region = current_app.config.get('AWS_REGION', 'us-east-1')
    use_ssl = current_app.config.get('S3_USE_SSL', False) 

    if not all([endpoint_url, access_key, secret_key]):
        logger.warning("Configuração S3/MinIO incompleta no app.config.")
        return None

    try:
        _s3_client = boto3.client(
            's3',
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region,
            config=Config(signature_version='s3v4'),
            use_ssl=use_ssl
        )
        logger.info(f"Cliente S3/MinIO configurado para endpoint: {endpoint_url}")
        return _s3_client
    except Exception as e:
        logger.error(f"Erro ao configurar cliente S3/MinIO: {e}", exc_info=True)
        return None

def upload_file_to_s3(local_file_path, bucket_name, object_name, content_type='video/mp4'):
    s3 = get_s3_client()
    if not s3:
        logger.error("Upload falhou: Cliente S3 não inicializado.")
        return False
    if not bucket_name:
        logger.error("Upload falhou: Nome do Bucket S3 não configurado.")
        return False

    try:
        logger.info(f"Fazendo upload de {local_file_path} para {bucket_name}/{object_name}...")
        extra_args = {'ContentType': content_type}
        s3.upload_file(local_file_path, bucket_name, object_name, ExtraArgs=extra_args)
        logger.info("Upload S3 concluído com sucesso.")
        return True
    except ClientError as e:
        logger.error(f"Erro de Cliente S3 durante upload para {bucket_name}/{object_name}: {e}", exc_info=True)
        return False
    except Exception as e:
        logger.error(f"Erro inesperado durante upload S3 para {bucket_name}/{object_name}: {e}", exc_info=True)
        return False