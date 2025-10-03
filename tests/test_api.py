"""
Unit tests for Flask API endpoints.

This module contains comprehensive tests for all CRUD operations
and API endpoints using pytest.
"""

import pytest
import json


class TestTaskAPI:
    """Test class for Task API endpoints."""
    
    def test_get_tasks_empty(self, client, init_database):
        """Test getting tasks when database is empty."""
        response = client.get('/api/tasks')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['count'] == 0
        assert len(data['data']) == 0
    
    def test_create_task(self, client, init_database):
        """Test creating a new task."""
        task_data = {
            'title': 'Test Task',
            'description': 'Test Description',
            'priority': 'High'
        }
        response = client.post(
            '/api/tasks',
            data=json.dumps(task_data),
            content_type='application/json'
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['title'] == 'Test Task'
        assert data['data']['priority'] == 'High'
        assert data['data']['completed'] is False
    
    def test_create_task_without_title(self, client, init_database):
        """Test creating task without title returns error."""
        task_data = {
            'description': 'Test Description'
        }
        response = client.post(
            '/api/tasks',
            data=json.dumps(task_data),
            content_type='application/json'
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
    
    def test_get_task_by_id(self, client, init_database):
        """Test getting a specific task by ID."""
        task_data = {'title': 'Test Task'}
        create_response = client.post(
            '/api/tasks',
            data=json.dumps(task_data),
            content_type='application/json'
        )
        task_id = json.loads(create_response.data)['data']['id']
        
        response = client.get(f'/api/tasks/{task_id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['id'] == task_id
    
    def test_get_nonexistent_task(self, client, init_database):
        """Test getting non-existent task returns 404."""
        response = client.get('/api/tasks/9999')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['success'] is False
    
    def test_update_task(self, client, init_database):
        """Test updating a task."""
        task_data = {'title': 'Original Title'}
        create_response = client.post(
            '/api/tasks',
            data=json.dumps(task_data),
            content_type='application/json'
        )
        task_id = json.loads(create_response.data)['data']['id']
        
        update_data = {
            'title': 'Updated Title',
            'completed': True,
            'priority': 'Low'
        }
        response = client.put(
            f'/api/tasks/{task_id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['title'] == 'Updated Title'
        assert data['data']['completed'] is True
        assert data['data']['priority'] == 'Low'
    
    def test_update_nonexistent_task(self, client, init_database):
        """Test updating non-existent task returns 404."""
        update_data = {'title': 'Updated Title'}
        response = client.put(
            '/api/tasks/9999',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        assert response.status_code == 404
    
    def test_delete_task(self, client, init_database):
        """Test deleting a task."""
        task_data = {'title': 'Task to Delete'}
        create_response = client.post(
            '/api/tasks',
            data=json.dumps(task_data),
            content_type='application/json'
        )
        task_id = json.loads(create_response.data)['data']['id']
        
        response = client.delete(f'/api/tasks/{task_id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        
        get_response = client.get(f'/api/tasks/{task_id}')
        assert get_response.status_code == 404
    
    def test_delete_nonexistent_task(self, client, init_database):
        """Test deleting non-existent task returns 404."""
        response = client.delete('/api/tasks/9999')
        assert response.status_code == 404
    
    def test_search_tasks(self, client, init_database):
        """Test searching tasks."""
        client.post('/api/tasks', 
                   data=json.dumps({'title': 'Python Project'}),
                   content_type='application/json')
        client.post('/api/tasks',
                   data=json.dumps({'title': 'Java Assignment'}),
                   content_type='application/json')
        
        response = client.get('/api/tasks/search?q=Python')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['count'] == 1
        assert 'Python' in data['data'][0]['title']
    
    def test_search_without_query(self, client, init_database):
        """Test searching without query returns error."""
        response = client.get('/api/tasks/search')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
    
    def test_filter_completed_tasks(self, client, init_database):
        """Test filtering tasks by completion status."""
        client.post('/api/tasks',
                   data=json.dumps({'title': 'Task 1'}),
                   content_type='application/json')
        
        create_response = client.post('/api/tasks',
                   data=json.dumps({'title': 'Task 2'}),
                   content_type='application/json')
        task_id = json.loads(create_response.data)['data']['id']
        
        client.put(f'/api/tasks/{task_id}',
                  data=json.dumps({'completed': True}),
                  content_type='application/json')
        
        response = client.get('/api/tasks?completed=true')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['count'] == 1
        assert data['data'][0]['completed'] is True
    
    def test_export_csv(self, client, init_database):
        """Test CSV export endpoint."""
        client.post('/api/tasks',
                   data=json.dumps({'title': 'Export Test'}),
                   content_type='application/json')
        
        response = client.get('/api/tasks/export/csv')
        assert response.status_code == 200
        assert response.content_type == 'text/csv; charset=utf-8'
    
    def test_export_json(self, client, init_database):
        """Test JSON export endpoint."""
        client.post('/api/tasks',
                   data=json.dumps({'title': 'Export Test'}),
                   content_type='application/json')
        
        response = client.get('/api/tasks/export/json')
        assert response.status_code == 200
        assert response.content_type == 'application/json'
    
    def test_root_endpoint(self, client):
        """Test API root endpoint."""
        response = client.get('/')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'message' in data
        assert 'endpoints' in data
    
    def test_health_endpoint(self, client):
        """Test health check endpoint."""
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
