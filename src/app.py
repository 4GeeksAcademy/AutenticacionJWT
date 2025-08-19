"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from werkzeug.security import generate_password_hash, check_password_hash

from api.utils import APIException, generate_sitemap
from api.models import db, User
from api.routes import api

app = Flask(__name__)
app.url_map.strict_slashes = False

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL", "sqlite:////tmp/auth.db"
).replace("postgres://", "postgresql://")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "change-this")

db.init_app(app)
Migrate(app, db)

CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

@app.after_request
def add_cors_headers(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return resp

jwt = JWTManager(app)
app.register_blueprint(api, url_prefix="/api")


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.route("/")
def health():
    return jsonify({"ok": True}), 200


@app.route("/signup", methods=["POST", "OPTIONS"])
def signup():
    if request.method == "OPTIONS":
        return ("", 204)
    body = request.get_json() or {}
    email = (body.get("email") or "").strip().lower()
    password = body.get("password") or ""
    if not email or not password:
        return jsonify({"msg": "email y password requeridos"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "email ya registrado"}), 409
    user = User(
        email=email,
        password=generate_password_hash(password),
        is_active=True
    )
    db.session.add(user)
    db.session.commit()
    return jsonify(user.serialize()), 201


@app.route("/token", methods=["POST", "OPTIONS"])
def token():
    if request.method == "OPTIONS":
        return ("", 204)
    body = request.get_json() or {}
    email = (body.get("email") or "").strip().lower()
    password = body.get("password") or ""
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"msg": "credenciales inválidas"}), 401
    access = create_access_token(identity=str(user.id))
    return jsonify({"access_token": access, "user": user.serialize()}), 200


@app.route("/private", methods=["GET", "OPTIONS"])
@jwt_required(optional=True)
def private():
    if request.method == "OPTIONS":
        return ("", 204)
    uid = get_jwt_identity()
    if not uid:
        return jsonify({"msg": "token requerido"}), 401
    user = User.query.get(int(uid))
    return jsonify({"ok": True, "user": user.serialize()}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 3001)), debug=True)
