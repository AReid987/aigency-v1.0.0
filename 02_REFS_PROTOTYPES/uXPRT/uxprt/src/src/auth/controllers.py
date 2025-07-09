from flask import jsonify
import bcrypt
import jwt
import os
from datetime import datetime, timedelta
from uuid import UUID

# TODO: Replace with actual database interaction using the chosen ORM
# from src.db.models import User

def token_required(f):
    # TODO: Implement actual token validation and user loading
    # from functools import wraps
    # @wraps(f)
    # def decorated(*args, **kwargs):
    #     print("Token validation skipped")
    #     return f(*args, **kwargs) # Placeholder for now
    return f

async def get_current_user_id():
    # Replace with actual logic to get user ID from authentication token/session
    # For now, returning a placeholder UUID
    return UUID("12345678-1234-5678-1234-567812345678") # Placeholder UUID

def hash_password(password):
    """Hashes a password using bcrypt."""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def check_password(password, hashed_password):
    """Checks if a password matches the hashed password."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def generate_token(user_id):
    """Generates a JWT token for a user."""
    # TODO: Use a more secure and configurable secret key
    secret_key = os.environ.get('JWT_SECRET_KEY', 'super-secret-key')
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=24)  # Token expires in 24 hours
    }
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token

def decode_token(token):
    """Decodes a JWT token."""
    secret_key = os.environ.get('JWT_SECRET_KEY', 'super-secret-key')
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None  # Token has expired
    except jwt.InvalidTokenError:
        return None  # Invalid token

def register_user(username, email, password):
    """Registers a new user."""
    # TODO: Implement actual user creation in the database
    # Example placeholder logic:
    # if User.find_by_email(email):
    #     return {"message": "User already exists"}, 409
    # hashed_password = hash_password(password)
    # new_user = User.create(username=username, email=email, password=hashed_password)
    # return {"message": "User registered successfully"}, 201
    print(f"Attempting to register user: {username}, {email}")
    return {"message": "Registration logic not implemented yet"}, 501 # Not Implemented

def login_user(email, password):
    """Logs in a user."""
    # TODO: Implement actual user login logic
    # Example placeholder logic:
    # user = User.find_by_email(email)
    # if user and check_password(password, user.password):
    #     token = generate_token(user.id)
    #     return {"token": token}, 200
    # else:
    #     return {"message": "Invalid credentials"}, 401
    print(f"Attempting to login user: {email}")
    return {"message": "Login logic not implemented yet"}, 501 # Not Implemented

def logout_user(token):
    """Logs out a user."""
    # TODO: Implement actual user logout logic (e.g., token invalidation)
    # For JWT, typically client-side token removal is sufficient,
    # but server-side invalidation is needed for true logout.
    user_id = decode_token(token)
    if user_id:
        print(f"User {user_id} logged out")
        return {"message": "User logged out successfully"}, 200