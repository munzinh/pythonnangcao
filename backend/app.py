"""
Flask Application Entry Point.

This is the main Flask application that initializes the database,
registers blueprints, and runs the development server.
"""

import os
import sys
from flask import Flask, jsonify
from flask_cors import CORS

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.config import config_by_name
from backend.database import init_db
from backend.routes import api_bp


def create_app(config_name='development'):
    """
    Application factory pattern for creating Flask app.
    
    Args:
        config_name (str): Configuration name (development, testing, production)
        
    Returns:
        Flask: Configured Flask application
    """
    app = Flask(__name__)
    
    config = config_by_name.get(config_name, config_by_name['default'])
    app.config.from_object(config)
    
    CORS(app)
    
    init_db(app)
    
    app.register_blueprint(api_bp)
    
    @app.route('/')
    def index():
        """API root endpoint."""
        return jsonify({
            'message': 'To-Do List API',
            'version': '1.0',
            'endpoints': {
                'tasks': '/api/tasks',
                'search': '/api/tasks/search?q=query',
                'export_csv': '/api/tasks/export/csv',
                'export_json': '/api/tasks/export/json'
            }
        })
    
    @app.route('/health')
    def health():
        """Health check endpoint."""
        return jsonify({
            'status': 'healthy',
            'database': 'connected'
        }), 200
    
    return app


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
