"""
Database seed script.

This script initializes the database and creates sample tasks
for testing and demonstration purposes.
"""

import os
import sys
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(__file__))

from backend.database import init_db, get_session, close_session
from backend.models import Task


def seed_database():
    """
    Seed database with sample tasks.
    
    Creates initial tasks with varying priorities and completion status
    for testing the application.
    """
    print("=" * 50)
    print("Initializing Database...")
    print("=" * 50)
    
    try:
        init_db()
        print("✓ Database initialized successfully")
    except Exception as e:
        print(f"✗ Error initializing database: {e}")
        return
    
    session = get_session()
    
    try:
        existing_count = session.query(Task).count()
        if existing_count > 0:
            print(f"\n⚠ Database already contains {existing_count} tasks")
            response = input("Do you want to clear and reseed? (y/n): ")
            if response.lower() != 'y':
                print("Seeding cancelled")
                return
            
            session.query(Task).delete()
            session.commit()
            print("✓ Existing tasks cleared")
        
        sample_tasks = [
            {
                'title': 'Hoàn thành báo cáo đồ án Python',
                'description': 'Viết báo cáo chi tiết về ứng dụng To-Do List, bao gồm ERD, flowchart và screenshots',
                'priority': 'High',
                'completed': False
            },
            {
                'title': 'Học bài Flask REST API',
                'description': 'Ôn tập các khái niệm về RESTful API, HTTP methods và JSON response',
                'priority': 'High',
                'completed': True
            },
            {
                'title': 'Viết unit tests cho API',
                'description': 'Tạo test cases cho tất cả endpoints sử dụng pytest',
                'priority': 'Medium',
                'completed': True
            },
            {
                'title': 'Cải thiện giao diện Tkinter',
                'description': 'Thêm màu sắc, icon và cải thiện UX cho ứng dụng',
                'priority': 'Low',
                'completed': False
            },
            {
                'title': 'Tìm hiểu SQLAlchemy ORM',
                'description': 'Học về models, relationships và query optimization',
                'priority': 'Medium',
                'completed': True
            },
            {
                'title': 'Chuẩn bị presentation đồ án',
                'description': 'Tạo slides PowerPoint để trình bày đồ án trước lớp',
                'priority': 'High',
                'completed': False
            },
            {
                'title': 'Review code và refactor',
                'description': 'Kiểm tra code quality, tuân thủ PEP8 và thêm docstring',
                'priority': 'Medium',
                'completed': False
            },
            {
                'title': 'Đọc tài liệu về Exception Handling',
                'description': 'Tìm hiểu cách xử lý lỗi hiệu quả trong Python',
                'priority': 'Low',
                'completed': True
            }
        ]
        
        print("\nCreating sample tasks...")
        print("-" * 50)
        
        for idx, task_data in enumerate(sample_tasks, 1):
            task = Task(**task_data)
            session.add(task)
            status = "✓" if task_data['completed'] else "○"
            print(f"{status} [{task_data['priority']:6}] {task_data['title']}")
        
        session.commit()
        
        print("-" * 50)
        print(f"\n✓ Successfully created {len(sample_tasks)} sample tasks")
        
        total = session.query(Task).count()
        completed = session.query(Task).filter(Task.completed == True).count()
        pending = total - completed
        
        print("\nDatabase Statistics:")
        print(f"  Total tasks: {total}")
        print(f"  Completed: {completed}")
        print(f"  Pending: {pending}")
        
        print("\n" + "=" * 50)
        print("Database seeding completed successfully!")
        print("=" * 50)
        print("\nNext steps:")
        print("1. Start backend: python backend/app.py")
        print("2. Start frontend: python frontend/gui.py")
        print("3. Run tests: pytest tests/")
        
    except Exception as e:
        session.rollback()
        print(f"\n✗ Error seeding database: {e}")
        import traceback
        traceback.print_exc()
    finally:
        close_session(session)


if __name__ == '__main__':
    seed_database()
