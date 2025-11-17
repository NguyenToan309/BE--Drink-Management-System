# shop_backend/routes/auth.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from extensions import db, bcrypt
from models import User
from sqlalchemy.exc import IntegrityError # Import để bắt lỗi double-click

auth_bp = Blueprint('auth', __name__)

# REGISTER
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({"message": "Missing required fields"}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({"message": "Email already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(
        name=data['username'],
        email=data['email'],
        password=hashed_password
    )
    db.session.add(new_user)
    
    try:
        db.session.commit()
    except IntegrityError: 
        db.session.rollback() 
        return jsonify({"message": "Email already exists (race condition)"}), 400

    # ----------------------------------------------------
    # ⬇️ SỬA LỖI 422 (Subject must be a string) ⬇️
    # ----------------------------------------------------
    token = create_access_token(identity=str(new_user.id)) # Dùng str()

    return jsonify({
        "token": token,
        "user": {"id": new_user.id, "email": new_user.email, "name": new_user.name}
    }), 200

# LOGIN
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data.get('email') or not data.get('password'):
        return jsonify({"message": "Missing email or password"}), 400

    user = User.query.filter_by(email=data['email']).first()

    if not user or not bcrypt.check_password_hash(user.password, data['password']):
        return jsonify({"message": "Invalid credentials"}), 401

    # ----------------------------------------------------
    # ⬇️ SỬA LỖI 422 (Subject must be a string) ⬇️
    # ----------------------------------------------------
    token = create_access_token(identity=str(user.id)) # Dùng str()

    return jsonify({
        "token": token,
        "user": {"id": user.id, "email": user.email, "name": user.name}
    }), 200