from flask import Blueprint, request, jsonify
from app.auth.controller import register_user, authenticate_user
from app.auth.utils import generate_token

bp = Blueprint("auth", __name__)

"""@bp.route("/register", methods=["POST"])
def register():
    data = request.json
    user, error = register_user(data['email'], data['password'])
    if error:
        return jsonify({"error": error}), 400
    return jsonify({"message": "User registered successfully"})
"""
@bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = authenticate_user(data['email'], data['password'])
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401
    token = generate_token(user.id)
    return jsonify({"token": token})

