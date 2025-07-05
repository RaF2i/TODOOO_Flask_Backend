# routes.py

from flask import Blueprint, request, jsonify, g
from .controllers import AuthController, TaskController
from .auth_decorator import token_required

api_bp = Blueprint('api', __name__, url_prefix='/api')

# --- Base Route ---
@api_bp.route('/', methods=['GET'])
def hello_world():
    return jsonify({'message': 'Hello from the API!'})

# --- Authentication Routes ---
@api_bp.route('/auth/register', methods=['POST'])
def register():
    result = AuthController.register(request.get_json())
    if not result['success']:
        return jsonify({'error': result['error']}), 400
    return jsonify(result), 201

@api_bp.route('/auth/login', methods=['POST'])
def login():
    result = AuthController.login(request.get_json())
    if not result['success']:
        return jsonify({'error': result['error']}), 401
    return jsonify(result)

# --- Task Routes ---
@api_bp.route('/tasks', methods=['GET'])
@token_required
def get_tasks():
    user_id = g.current_user.id
    result = TaskController.get_user_tasks(user_id)
    return jsonify(result)

@api_bp.route('/tasks', methods=['POST'])
@token_required
def create_task():
    user_id = g.current_user.id
    result = TaskController.create_task(user_id, request.get_json())
    if not result['success']:
        return jsonify({'error': result['error']}), 400
    return jsonify(result), 201

@api_bp.route('/tasks/<int:task_id>', methods=['PUT'])
@token_required
def update_task(task_id):
    user_id = g.current_user.id
    result = TaskController.update_task(task_id, user_id, request.get_json())
    if not result['success']:
        return jsonify({'error': result['error']}), 404 # Use 404 for not found
    return jsonify(result)

@api_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
@token_required
def delete_task(task_id):
    user_id = g.current_user.id
    result = TaskController.delete_task(task_id, user_id)
    if not result['success']:
        return jsonify({'error': result['error']}), 404
    return jsonify(result)

@api_bp.route('/tasks/<int:task_id>/toggle', methods=['PATCH'])
@token_required
def toggle_task(task_id):
    user_id = g.current_user.id
    result = TaskController.toggle_task_complete(task_id, user_id)
    if not result['success']:
        return jsonify({'error': result['error']}), 404
    return jsonify(result)