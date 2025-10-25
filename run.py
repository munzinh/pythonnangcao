"""
Flask Application Entry Point.

This is the main entry point for the Flask application.
It creates the app instance and runs the development server.
"""

import os
from app import create_app

# Create the Flask application
app = create_app()

if __name__ == '__main__':
    # Get configuration from environment
    env = os.getenv('FLASK_ENV', 'development')
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', '5000'))
    
    print("=" * 60)
    print("TaskMaster - Todo List Application")
    print("=" * 60)
    print(f"Environment: {env}")
    print(f"Debug Mode: {debug}")
    print(f"Database: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print("=" * 60)
    print("Available Endpoints:")
    print("  Web Interface: http://localhost:5000/")
    print("  API Endpoints:")
    print("    - GET    /api/tasks")
    print("    - POST   /api/tasks")
    print("    - GET    /api/tasks/<id>")
    print("    - PUT    /api/tasks/<id>")
    print("    - DELETE /api/tasks/<id>")
    print("    - GET    /api/tasks/search?q=<query>")
    print("    - GET    /api/tasks/export/csv")
    print("    - GET    /api/tasks/export/json")
    print("=" * 60)
    print("Starting server...")
    print("=" * 60)
    
    # Run the application
    app.run(host=host, port=port, debug=debug)
