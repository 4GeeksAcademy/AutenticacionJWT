"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
# api/routes.py
from flask import Blueprint, request, jsonify
from flask_cors import CORS
from api.models import db, User
from api.utils import APIException
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from werkzeug.security import generate_password_hash, check_password_hash

api = Blueprint("api", __name__)
CORS(api)

@api.route("/signup", methods=["POST"])
def signup():
    body = request.get_json() or {}
    email = (body.get("email") or "").strip().lower()
    password = body.get("password") or ""

    if not email or not password:
        raise APIException("email and password are required", 400)

    if User.query.filter_by(email=email).first():
        raise APIException("email already exists", 409)

    user = User(email=email, password=generate_password_hash(password), is_active=True)
    db.session.add(user)
    db.session.commit()
    return jsonify({"id": user.id, "email": user.email}), 201


@api.route("/token", methods=["POST"])
def create_token():
    body = request.get_json() or {}
    email = (body.get("email") or "").strip().lower()
    password = body.get("password") or ""

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        raise APIException("bad credentials", 401)

    access_token = create_access_token(identity=user.id)
    return jsonify({"access_token": access_token}), 200


@api.route("/private", methods=["GET"])
@jwt_required()
def private():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return jsonify({"user": user.serialize()}), 200


@api.route("/hello", methods=["GET", "POST"])
def handle_hello():
    return jsonify({"message": "Hello from the API"}), 200
