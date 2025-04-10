import jwt
from datetime import datetime, timedelta
from flask import current_app, request
from functools import wraps

def generate_token(user_id, expires_in=3600):
    payload = {
        'user_id': user_id,
        'exp': datetime.now() + timedelta(seconds=expires_in)
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

def verify_token(token):
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload['user_id']
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None
