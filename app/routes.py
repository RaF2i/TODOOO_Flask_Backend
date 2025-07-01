# This file defines all the API endpoints.

from flask import Blueprint, request, jsonify, g
from .controllers import AuthController, TaskController
from .auth_decorator import token_required

# Create a Blueprint for API routes
api_bp = Blueprint('api', __name__, url_prefix='/api')

# --- Base Route ---

@api_bp.route('/', methods=['GET'])
def hello_world():
    return jsonify({'message': 'Hello World!'})

# --- Authentication Routes ---

@api_bp.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    result = AuthController.register(data)
    if not result['success']:
        return jsonify({'error': result['error']}), 400
    return jsonify(result), 201

@api_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    result = AuthController.login(data)
    if not result['success']:
        return jsonify({'error': result['error']}), 401
    return jsonify(result)

# --- Task Routes ---

@api_bp.route('/tasks', methods=['GET'])
@token_required
def get_tasks():
    # The user's ID is retrieved from the global context `g`,
    # which was set by the @token_required decorator.
    user_id = g.current_user['id']
    result = TaskController.get_user_tasks(user_id)
    return jsonify(result)

@api_bp.route('/tasks', methods=['POST'])
@token_required
def create_task():
    user_id = g.current_user['id']
    data = request.get_json()
    result = TaskController.create_task(user_id, data)
    if not result['success']:
        return jsonify({'error': result['error']}), 400
    return jsonify(result), 201

@api_bp.route('/tasks/<int:task_id>', methods=['PUT'])
@token_required
def update_task(task_id):
    # Note: A security improvement here would be to verify that the task
    # with `task_id` actually belongs to the authenticated user.
    data = request.get_json()
    result = TaskController.update_task(task_id, data)
    if not result['success']:
        return jsonify({'error': result['error']}), 400
    return jsonify(result)

@api_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
@token_required
def delete_task(task_id):
    result = TaskController.delete_task(task_id)
    if not result['success']:
        return jsonify({'error': result['error']}), 400
    return jsonify(result)

@api_bp.route('/tasks/<int:task_id>/toggle', methods=['PATCH'])
@token_required
def toggle_task(task_id):
    result = TaskController.toggle_task_complete(task_id)
    if not result['success']:
        return jsonify({'error': result['error']}), 400
    return jsonify(result)