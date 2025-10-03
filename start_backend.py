#!/usr/bin/env python3
"""
Backend startup script.

This script sets up the Python path and starts the Flask backend server.
"""

import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Now import and run the app
from backend.app import create_app
import os

if __name__ == '__main__':
    env = os.getenv('FLASK_ENV', 'development')
    app = create_app(env)
    
    print("=" * 50)
    print("To-Do List API Server Starting...")
    print(f"Environment: {env}")
    print(f"Database: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print("API Endpoints:")
    print("  - GET    /api/tasks")
    print("  - POST   /api/tasks")
    print("  - GET    /api/tasks/<id>")
    print("  - PUT    /api/tasks/<id>")
    print("  - DELETE /api/tasks/<id>")
    print("  - GET    /api/tasks/search?q=<query>")
    print("  - GET    /api/tasks/export/csv")
    print("  - GET    /api/tasks/export/json")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
