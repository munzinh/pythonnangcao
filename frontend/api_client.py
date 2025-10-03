"""
API Client for communicating with Flask backend.

This module handles all HTTP requests to the REST API with proper
error handling and response parsing.
"""

import requests
import os
from typing import Optional, Dict, List
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class APIClient:
    """
    API Client class for backend communication.
    
    Attributes:
        base_url (str): Base URL of the API server
    """
    
    def __init__(self, base_url: Optional[str] = None):
        """
        Initialize API client.
        
        Args:
            base_url (str, optional): API base URL, defaults to localhost:5000
        """
        self.base_url = base_url or os.getenv('API_BASE_URL', 'http://localhost:5000')
        
        # Tối ưu: Tạo session với connection pooling
        self.session = requests.Session()
        
        # Cấu hình retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=0.1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        
        adapter = HTTPAdapter(
            max_retries=retry_strategy,
            pool_connections=10,
            pool_maxsize=20
        )
        
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
    
    def _handle_response(self, response: requests.Response) -> Dict:
        """
        Handle API response and extract data.
        
        Args:
            response: HTTP response object
            
        Returns:
            dict: Response data
            
        Raises:
            Exception: For API errors
        """
        try:
            data = response.json()
            if not data.get('success', False):
                raise Exception(data.get('error', 'Unknown error'))
            return data
        except requests.exceptions.JSONDecodeError:
            raise Exception("Invalid response from server")
    
    def get_tasks(self, completed: Optional[bool] = None) -> List[Dict]:
        """
        Get all tasks.
        
        Args:
            completed (bool, optional): Filter by completion status
            
        Returns:
            list: List of tasks
            
        Raises:
            Exception: For connection or API errors
        """
        try:
            params = {}
            if completed is not None:
                params['completed'] = str(completed).lower()
            
            response = self.session.get(
                f"{self.base_url}/api/tasks",
                params=params,
                timeout=5
            )
            data = self._handle_response(response)
            return data.get('data', [])
        except requests.exceptions.ConnectionError:
            raise Exception("Cannot connect to server. Make sure backend is running.")
        except requests.exceptions.Timeout:
            raise Exception("Request timeout. Server not responding.")
        except Exception as e:
            raise Exception(f"Error getting tasks: {str(e)}")
    
    def create_task(self, title: str, description: str = '', priority: str = 'Medium') -> Dict:
        """
        Create a new task.
        
        Args:
            title (str): Task title
            description (str, optional): Task description
            priority (str, optional): Task priority
            
        Returns:
            dict: Created task data
            
        Raises:
            Exception: For API errors
        """
        try:
            response = self.session.post(
                f"{self.base_url}/api/tasks",
                json={
                    'title': title,
                    'description': description,
                    'priority': priority
                },
                timeout=5
            )
            data = self._handle_response(response)
            return data.get('data', {})
        except Exception as e:
            raise Exception(f"Error creating task: {str(e)}")
    
    def update_task(self, task_id: int, **kwargs) -> Dict:
        """
        Update a task.
        
        Args:
            task_id (int): Task ID
            **kwargs: Fields to update
            
        Returns:
            dict: Updated task data
            
        Raises:
            Exception: For API errors
        """
        try:
            response = self.session.put(
                f"{self.base_url}/api/tasks/{task_id}",
                json=kwargs,
                timeout=5
            )
            data = self._handle_response(response)
            return data.get('data', {})
        except Exception as e:
            raise Exception(f"Error updating task: {str(e)}")
    
    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task.
        
        Args:
            task_id (int): Task ID
            
        Returns:
            bool: True if deleted successfully
            
        Raises:
            Exception: For API errors
        """
        try:
            response = self.session.delete(
                f"{self.base_url}/api/tasks/{task_id}",
                timeout=5
            )
            self._handle_response(response)
            return True
        except Exception as e:
            raise Exception(f"Error deleting task: {str(e)}")
    
    def search_tasks(self, query: str) -> List[Dict]:
        """
        Search tasks.
        
        Args:
            query (str): Search query
            
        Returns:
            list: List of matching tasks
            
        Raises:
            Exception: For API errors
        """
        try:
            response = self.session.get(
                f"{self.base_url}/api/tasks/search",
                params={'q': query},
                timeout=5
            )
            data = self._handle_response(response)
            return data.get('data', [])
        except Exception as e:
            raise Exception(f"Error searching tasks: {str(e)}")
    
    def export_csv(self, filepath: str) -> bool:
        """
        Export tasks to CSV file.
        
        Args:
            filepath (str): Path to save CSV file
            
        Returns:
            bool: True if exported successfully
            
        Raises:
            Exception: For API or file errors
        """
        try:
            response = self.session.get(
                f"{self.base_url}/api/tasks/export/csv",
                timeout=10
            )
            
            if response.status_code == 200:
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                return True
            else:
                raise Exception("Export failed")
        except Exception as e:
            raise Exception(f"Error exporting CSV: {str(e)}")
    
    def export_json(self, filepath: str) -> bool:
        """
        Export tasks to JSON file.
        
        Args:
            filepath (str): Path to save JSON file
            
        Returns:
            bool: True if exported successfully
            
        Raises:
            Exception: For API or file errors
        """
        try:
            response = self.session.get(
                f"{self.base_url}/api/tasks/export/json",
                timeout=10
            )
            
            if response.status_code == 200:
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                return True
            else:
                raise Exception("Export failed")
        except Exception as e:
            raise Exception(f"Error exporting JSON: {str(e)}")
