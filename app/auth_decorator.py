# auth_decorator.py

from functools import wraps
from flask import request, jsonify, g
import jwt
import os
from .models import User

def token_required(f):
    """
    Decorator to ensure a valid JWT is present in the request header.
    It decodes the token and attaches the user model instance to the global `g` object.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'authorization' in request.headers:
            auth_header = request.headers['authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(" ")[1]

        if not token:
            return jsonify({'error': 'Authentication required'}), 401

        try:
            data = jwt.decode(token, os.environ.get('JWT_SECRET'), algorithms=["HS256"])
            # Use SQLAlchemy's query.get() for primary key lookup
            current_user = User.query.get(data['userId'])
            if not current_user:
                return jsonify({'error': 'User not found'}), 401
            # Attach the user object to the global context `g`
            g.current_user = current_user

        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(*args, **kwargs)

    return decorated