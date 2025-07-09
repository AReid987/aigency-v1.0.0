from flask import Blueprint, request, jsonify
from .controllers import register_user, login_user, logout_user, decode_token

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"message": "Missing required fields"}), 400

    message, status_code = register_user(username, email, password)
    return jsonify(message), status_code

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message": "Missing required fields"}), 400

    message, status_code = login_user(email, password)
    return jsonify(message), status_code

@auth_bp.route('/logout', methods=['POST'])
def logout():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"message": "Authentication required"}), 401

    try:
        token = auth_header.split(' ')[1]
        message, status_code = logout_user(token)
        return jsonify(message), status_code
    except IndexError:
        return jsonify({"message": "Invalid token format"}), 401

# Middleware to protect routes
pass