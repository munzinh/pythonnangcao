"""
Database models using SQLAlchemy ORM.

This module defines the Task model and TaskManager class for CRUD operations.
Implements OOP principles with proper encapsulation and abstraction.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from backend.database import Base, get_session, close_session


class Task(Base):
    """
    Task model representing a to-do item.
    
    Attributes:
        id (int): Primary key
        title (str): Task title (required)
        description (str): Detailed task description
        completed (bool): Completion status
        priority (str): Task priority (Low, Medium, High)
        created_at (datetime): Creation timestamp
        updated_at (datetime): Last update timestamp
    """
    
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    completed = Column(Boolean, default=False, nullable=False)
    priority = Column(String(20), default='Medium')
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        """
        Convert Task object to dictionary.
        
        Returns:
            dict: Task data as dictionary
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'priority': self.priority,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        """String representation of Task."""
        return f"<Task(id={self.id}, title='{self.title}', completed={self.completed})>"


class TaskManager:
    """
    Task Manager class implementing business logic for CRUD operations.
    
    This class follows OOP principles with proper error handling and
    session management.
    """
    
    @staticmethod
    def create_task(title, description=None, priority='Medium'):
        """
        Create a new task.
        
        Args:
            title (str): Task title
            description (str, optional): Task description
            priority (str, optional): Task priority (Low, Medium, High)
            
        Returns:
            dict: Created task data or None if failed
            
        Raises:
            ValueError: If title is empty
            Exception: For database errors
        """
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty")
        
        session = get_session()
        try:
            task = Task(
                title=title.strip(),
                description=description.strip() if description else None,
                priority=priority
            )
            session.add(task)
            session.commit()
            session.refresh(task)
            return task.to_dict()
        except Exception as e:
            session.rollback()
            print(f"Error creating task: {str(e)}")
            raise
        finally:
            close_session(session)
    
    @staticmethod
    def get_all_tasks(completed=None):
        """
        Get all tasks with optional filtering.
        
        Args:
            completed (bool, optional): Filter by completion status
            
        Returns:
            list: List of task dictionaries
        """
        session = get_session()
        try:
            query = session.query(Task)
            if completed is not None:
                query = query.filter(Task.completed == completed)
            tasks = query.order_by(Task.created_at.desc()).all()
            return [task.to_dict() for task in tasks]
        except Exception as e:
            print(f"Error getting tasks: {str(e)}")
            return []
        finally:
            close_session(session)
    
    @staticmethod
    def get_task_by_id(task_id):
        """
        Get a specific task by ID.
        
        Args:
            task_id (int): Task ID
            
        Returns:
            dict: Task data or None if not found
        """
        session = get_session()
        try:
            task = session.query(Task).filter(Task.id == task_id).first()
            return task.to_dict() if task else None
        except Exception as e:
            print(f"Error getting task: {str(e)}")
            return None
        finally:
            close_session(session)
    
    @staticmethod
    def update_task(task_id, **kwargs):
        """
        Update a task with provided fields.
        
        Args:
            task_id (int): Task ID
            **kwargs: Fields to update (title, description, completed, priority)
            
        Returns:
            dict: Updated task data or None if not found
            
        Raises:
            ValueError: If invalid data provided
            Exception: For database errors
        """
        session = get_session()
        try:
            task = session.query(Task).filter(Task.id == task_id).first()
            if not task:
                return None
            
            if 'title' in kwargs:
                if not kwargs['title'] or not kwargs['title'].strip():
                    raise ValueError("Task title cannot be empty")
                task.title = kwargs['title'].strip()
            
            if 'description' in kwargs:
                task.description = kwargs['description'].strip() if kwargs['description'] else None
            
            if 'completed' in kwargs:
                task.completed = bool(kwargs['completed'])
            
            if 'priority' in kwargs:
                task.priority = kwargs['priority']
            
            task.updated_at = datetime.utcnow()
            session.commit()
            session.refresh(task)
            return task.to_dict()
        except Exception as e:
            session.rollback()
            print(f"Error updating task: {str(e)}")
            raise
        finally:
            close_session(session)
    
    @staticmethod
    def delete_task(task_id):
        """
        Delete a task by ID.
        
        Args:
            task_id (int): Task ID
            
        Returns:
            bool: True if deleted, False if not found
            
        Raises:
            Exception: For database errors
        """
        session = get_session()
        try:
            task = session.query(Task).filter(Task.id == task_id).first()
            if not task:
                return False
            
            session.delete(task)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Error deleting task: {str(e)}")
            raise
        finally:
            close_session(session)
    
    @staticmethod
    def search_tasks(query):
        """
        Search tasks by title or description.
        
        Args:
            query (str): Search query
            
        Returns:
            list: List of matching task dictionaries
        """
        session = get_session()
        try:
            search_pattern = f"%{query}%"
            tasks = session.query(Task).filter(
                (Task.title.like(search_pattern)) | 
                (Task.description.like(search_pattern))
            ).order_by(Task.created_at.desc()).all()
            return [task.to_dict() for task in tasks]
        except Exception as e:
            print(f"Error searching tasks: {str(e)}")
            return []
        finally:
            close_session(session)
