from app.models.user import User
from app.extensions import db

def register_user(email, password):
    if User.query.filter_by(email=email).first():
        return None, "Email already registered"
    
    user = User(email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user, None

def authenticate_user(email, password):
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        return user
    return None
