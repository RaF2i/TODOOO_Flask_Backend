# This file defines the decorator to protect routes that require authentication.

from functools import wraps
from flask import request, jsonify, g
import jwt
import os
from .models import User

def token_required(f):
    """
    Decorator to ensure a valid JWT is present in the request header.
    It decodes the token and attaches the user's data to the global `g` object.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # Check for the 'Authorization' header
        if 'authorization' in request.headers:
            auth_header = request.headers['authorization']
            # The header should be in the format 'Bearer <token>'
            if auth_header.startswith('Bearer '):
                token = auth_header.split(" ")[1]

        if not token:
            return jsonify({'error': 'Authentication required'}), 401

        try:
            # Decode the token using the secret key
            data = jwt.decode(token, os.environ.get('JWT_SECRET'), algorithms=["HS256"])
            # Find the user based on the user ID from the token
            current_user = User.find_by_id(data['userId'])
            if not current_user:
                 return jsonify({'error': 'User not found'}), 401
            # Attach user data to the global context `g` for access in the route
            g.current_user = current_user

        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        
        # Proceed to the original route function
        return f(*args, **kwargs)

    return decorated

