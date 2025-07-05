# controllers.py

import bcrypt
import jwt
import os
import datetime
from .models import User, Task
from . import db

class AuthController:
    @staticmethod
    def register(data):
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')

        if not all([email, password, name]):
            return {'success': False, 'error': 'Email, password, and name are required'}

        if User.query.filter_by(email=email).first():
            return {'success': False, 'error': 'User already exists with this email'}

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(12))
        
        new_user = User(email=email, password=hashed_password.decode('utf-8'), name=name)
        db.session.add(new_user)
        db.session.commit()

        token = jwt.encode({
            'userId': new_user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
        }, os.environ.get('JWT_SECRET'), algorithm="HS256")

        return {'success': True, 'user': new_user.to_dict(), 'token': token}

    @staticmethod
    def login(data):
        email = data.get('email')
        password = data.get('password')

        if not all([email, password]):
            return {'success': False, 'error': 'Email and password are required'}

        user = User.query.filter_by(email=email).first()

        if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return {'success': False, 'error': 'Invalid email or password'}

        token = jwt.encode({
            'userId': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
        }, os.environ.get('JWT_SECRET'), algorithm="HS256")

        return {'success': True, 'user': user.to_dict(), 'token': token}

class TaskController:
    @staticmethod
    def get_user_tasks(user_id):
        tasks = Task.query.filter_by(user_id=user_id).order_by(Task.created_at.desc()).all()
        return {'success': True, 'tasks': [task.to_dict() for task in tasks]}

    @staticmethod
    def create_task(user_id, data):
        title = data.get('title')
        if not title:
            return {'success': False, 'error': 'Title is required'}

        new_task = Task(
            title=title, 
            description=data.get('description', ''), 
            user_id=user_id
        )
        db.session.add(new_task)
        db.session.commit()
        return {'success': True, 'task': new_task.to_dict()}

    @staticmethod
    def update_task(task_id, user_id, data):
        task = Task.query.filter_by(id=task_id, user_id=user_id).first()
        if not task:
            return {'success': False, 'error': 'Task not found or permission denied'}
        
        task.title = data.get('title', task.title)
        task.description = data.get('description', task.description)
        task.completed = data.get('completed', task.completed)
        db.session.commit()
        return {'success': True, 'task': task.to_dict()}

    @staticmethod
    def delete_task(task_id, user_id):
        task = Task.query.filter_by(id=task_id, user_id=user_id).first()
        if not task:
            return {'success': False, 'error': 'Task not found or permission denied'}
        
        db.session.delete(task)
        db.session.commit()
        return {'success': True, 'message': 'Task deleted successfully'}

    @staticmethod
    def toggle_task_complete(task_id, user_id):
        task = Task.query.filter_by(id=task_id, user_id=user_id).first()
        if not task:
            return {'success': False, 'error': 'Task not found or permission denied'}

        task.completed = not task.completed
        db.session.commit()
        return {'success': True, 'task': task.to_dict()}