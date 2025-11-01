"""
API endpoint cho các thao tác CRUD và tìm kiếm Task (Todo).
Các hàm đều trả về JSON rõ ràng, dễ thuyết trình.
"""
import csv, json, os
from flask import request, jsonify, send_file
from app.api import bp  # Blueprint cho nhóm route API
from app.models import TaskManager
from datetime import datetime

# Lấy danh sách task (có filter completed tuỳ chọn)
@bp.route('/tasks', methods=['GET'])
def get_tasks():
    try:
        completed = request.args.get('completed')
        if completed is not None:
            completed = completed.lower() == 'true'  # Chuẩn hoá bool
        tasks = TaskManager.get_all_tasks(completed=completed)
        return jsonify({'success': True, 'data': tasks, 'count': len(tasks)}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Lấy 1 task cụ thể theo ID
@bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    try:
        task = TaskManager.get_task_by_id(task_id)
        if task:
            return jsonify({'success': True, 'data': task}), 200
        return jsonify({'success': False, 'error': 'Task not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Thêm task mới
@bp.route('/tasks', methods=['POST'])
def create_task():
    try:
        data = request.get_json()
        if not data or 'title' not in data:
            return jsonify({'success': False, 'error': 'Title is required'}), 400
        task = TaskManager.create_task(
            title=data['title'],
            description=data.get('description'),
            priority=data.get('priority', 'Medium')
        )
        return jsonify({'success': True, 'data': task, 'message': 'Task created successfully'}), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Chỉnh sửa task qua ID
@bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        task = TaskManager.update_task(task_id, **data)
        if task:
            return jsonify({'success': True, 'data': task, 'message': 'Task updated successfully'}), 200
        else:
            return jsonify({'success': False, 'error': 'Task not found'}), 404
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Xoá 1 task
@bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        deleted = TaskManager.delete_task(task_id)
        if deleted:
            return jsonify({'success': True, 'message': 'Task deleted successfully'}), 200
        else:
            return jsonify({'success': False, 'error': 'Task not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Tìm kiếm task (theo tiêu đề/mô tả)
@bp.route('/tasks/search', methods=['GET'])
def search_tasks():
    try:
        query = request.args.get('q', '')
        if not query:
            return jsonify({'success': False, 'error': 'Search query is required'}), 400
        tasks = TaskManager.search_tasks(query)
        return jsonify({'success': True, 'data': tasks, 'count': len(tasks), 'query': query}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Xuất CSV danh sách task
@bp.route('/tasks/export/csv', methods=['GET'])
def export_csv():
    try:
        tasks = TaskManager.get_all_tasks()
        filename = f'tasks_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        temp_dir = os.path.join(os.getcwd(), 'temp')
        os.makedirs(temp_dir, exist_ok=True)
        filepath = os.path.join(temp_dir, filename)
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            if tasks:
                fieldnames = ['id', 'title', 'description', 'completed', 'priority', 'created_at', 'updated_at']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(tasks)
        def remove_file(response):
            try: os.remove(filepath)
            except: pass
            return response
        return remove_file(send_file(filepath, mimetype='text/csv', as_attachment=True, download_name=filename))
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Xuất JSON danh sách task
@bp.route('/tasks/export/json', methods=['GET'])
def export_json():
    try:
        tasks = TaskManager.get_all_tasks()
        filename = f'tasks_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        temp_dir = os.path.join(os.getcwd(), 'temp')
        os.makedirs(temp_dir, exist_ok=True)
        filepath = os.path.join(temp_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as jsonfile:
            json.dump({'exported_at': datetime.now().isoformat(),'total_tasks': len(tasks),'tasks': tasks}, jsonfile, indent=2, ensure_ascii=False)
        def remove_file(response):
            try: os.remove(filepath)
            except: pass
            return response
        return remove_file(send_file(filepath, mimetype='application/json', as_attachment=True, download_name=filename))
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Custom lỗi 404 cho API
@bp.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'error': 'Endpoint not found'}), 404

# Custom lỗi 500 cho API
@bp.errorhandler(500)
def internal_error(error):
    return jsonify({'success': False, 'error': 'Internal server error'}), 500
