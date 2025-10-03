"""
API Routes for Task CRUD operations.

This module defines REST API endpoints with proper error handling
and JSON response formatting.
"""

import csv
import json
import os
from flask import Blueprint, request, jsonify, send_file
from backend.models import TaskManager
from datetime import datetime

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/tasks', methods=['GET'])
def get_tasks():
    """
    Get all tasks with optional filtering.
    
    Query Parameters:
        completed (bool, optional): Filter by completion status
        
    Returns:
        JSON: List of tasks
    """
    try:
        completed = request.args.get('completed')
        if completed is not None:
            completed = completed.lower() == 'true'
        
        tasks = TaskManager.get_all_tasks(completed=completed)
        return jsonify({
            'success': True,
            'data': tasks,
            'count': len(tasks)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """
    Get a specific task by ID.
    
    Args:
        task_id (int): Task ID
        
    Returns:
        JSON: Task data or error
    """
    try:
        task = TaskManager.get_task_by_id(task_id)
        if task:
            return jsonify({
                'success': True,
                'data': task
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Task not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/tasks', methods=['POST'])
def create_task():
    """
    Create a new task.
    
    Request Body (JSON):
        title (str): Task title (required)
        description (str, optional): Task description
        priority (str, optional): Task priority (Low, Medium, High)
        
    Returns:
        JSON: Created task data
    """
    try:
        data = request.get_json()
        
        if not data or 'title' not in data:
            return jsonify({
                'success': False,
                'error': 'Title is required'
            }), 400
        
        task = TaskManager.create_task(
            title=data['title'],
            description=data.get('description'),
            priority=data.get('priority', 'Medium')
        )
        
        return jsonify({
            'success': True,
            'data': task,
            'message': 'Task created successfully'
        }), 201
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """
    Update a task.
    
    Args:
        task_id (int): Task ID
        
    Request Body (JSON):
        title (str, optional): Task title
        description (str, optional): Task description
        completed (bool, optional): Completion status
        priority (str, optional): Task priority
        
    Returns:
        JSON: Updated task data
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        task = TaskManager.update_task(task_id, **data)
        
        if task:
            return jsonify({
                'success': True,
                'data': task,
                'message': 'Task updated successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Task not found'
            }), 404
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """
    Delete a task.
    
    Args:
        task_id (int): Task ID
        
    Returns:
        JSON: Success message or error
    """
    try:
        deleted = TaskManager.delete_task(task_id)
        
        if deleted:
            return jsonify({
                'success': True,
                'message': 'Task deleted successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Task not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/tasks/search', methods=['GET'])
def search_tasks():
    """
    Search tasks by title or description.
    
    Query Parameters:
        q (str): Search query
        
    Returns:
        JSON: List of matching tasks
    """
    try:
        query = request.args.get('q', '')
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'Search query is required'
            }), 400
        
        tasks = TaskManager.search_tasks(query)
        return jsonify({
            'success': True,
            'data': tasks,
            'count': len(tasks),
            'query': query
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/tasks/export/csv', methods=['GET'])
def export_csv():
    """
    Export all tasks to CSV file.
    
    Returns:
        File: CSV file download
    """
    try:
        tasks = TaskManager.get_all_tasks()
        
        filename = f'tasks_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        # Tạo thư mục temp nếu chưa có
        temp_dir = os.path.join(os.getcwd(), 'temp')
        os.makedirs(temp_dir, exist_ok=True)
        filepath = os.path.join(temp_dir, filename)
        
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            if tasks:
                fieldnames = ['id', 'title', 'description', 'completed', 'priority', 'created_at', 'updated_at']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(tasks)
        
        # Gửi file và xóa sau khi gửi
        def remove_file(response):
            try:
                os.remove(filepath)
            except:
                pass
            return response
        
        return remove_file(send_file(
            filepath,
            mimetype='text/csv',
            as_attachment=True,
            download_name=filename
        ))
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/tasks/export/json', methods=['GET'])
def export_json():
    """
    Export all tasks to JSON file.
    
    Returns:
        File: JSON file download
    """
    try:
        tasks = TaskManager.get_all_tasks()
        
        filename = f'tasks_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        # Tạo thư mục temp nếu chưa có
        temp_dir = os.path.join(os.getcwd(), 'temp')
        os.makedirs(temp_dir, exist_ok=True)
        filepath = os.path.join(temp_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as jsonfile:
            json.dump({
                'exported_at': datetime.now().isoformat(),
                'total_tasks': len(tasks),
                'tasks': tasks
            }, jsonfile, indent=2, ensure_ascii=False)
        
        # Gửi file và xóa sau khi gửi
        def remove_file(response):
            try:
                os.remove(filepath)
            except:
                pass
            return response
        
        return remove_file(send_file(
            filepath,
            mimetype='application/json',
            as_attachment=True,
            download_name=filename
        ))
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@api_bp.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500
