# This file contains the business logic, separated from the routes.

import bcrypt
import jwt
import os
import datetime
from .models import User, Task

class AuthController:
    @staticmethod
    def register(data):
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')

        if not all([email, password, name]):
            return {'success': False, 'error': 'Email, password, and name are required'}

        if User.find_by_email(email):
            return {'success': False, 'error': 'User already exists with this email'}

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(12))

        # Create user in the database
        user = User.create(email, hashed_password.decode('utf-8'), name)
        if not user:
            return {'success': False, 'error': 'Failed to create user'}

        # Generate JWT token
        token = jwt.encode({
            'userId': user['id'],
            'email': user['email'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
        }, os.environ.get('JWT_SECRET'), algorithm="HS256")

        return {
            'success': True,
            'user': {'id': user['id'], 'email': user['email'], 'name': user['name']},
            'token': token
        }

    @staticmethod
    def login(data):
        email = data.get('email')
        password = data.get('password')

        if not all([email, password]):
            return {'success': False, 'error': 'Email and password are required'}

        user = User.find_by_email(email)
        if not user:
            return {'success': False, 'error': 'Invalid email or password'}

        # Check if the provided password matches the hashed password in the database
        if not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            return {'success': False, 'error': 'Invalid email or password'}

        # Generate JWT token
        token = jwt.encode({
            'userId': user['id'],
            'email': user['email'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
        }, os.environ.get('JWT_SECRET'), algorithm="HS256")

        return {
            'success': True,
            'user': {'id': user['id'], 'email': user['email'], 'name': user['name']},
            'token': token
        }

class TaskController:
    @staticmethod
    def get_user_tasks(user_id):
        tasks = Task.find_by_user_id(user_id)
        return {'success': True, 'tasks': tasks}

    @staticmethod
    def create_task(user_id, data):
        title = data.get('title')
        description = data.get('description', '')
        if not title:
            return {'success': False, 'error': 'Title is required'}
        
        task = Task.create(user_id, title, description)
        if not task:
            return {'success': False, 'error': 'Failed to create task'}
        
        return {'success': True, 'task': task}

    @staticmethod
    def update_task(task_id, data):
        title = data.get('title')
        description = data.get('description', '')
        completed = data.get('completed', False)
        if not title:
            return {'success': False, 'error': 'Title is required'}

        task = Task.update(task_id, title, description, completed)
        if not task:
            return {'success': False, 'error': 'Task not found or failed to update'}
        
        return {'success': True, 'task': task}

    @staticmethod
    def delete_task(task_id):
        if not Task.delete(task_id):
            return {'success': False, 'error': 'Task not found'}
        return {'success': True, 'message': 'Task deleted successfully'}

    @staticmethod
    def toggle_task_complete(task_id):
        task = Task.toggle_complete(task_id)
        if not task:
            return {'success': False, 'error': 'Task not found'}
        return {'success': True, 'task': task}
