"""
Flask Application Factory.

This module creates and configures the Flask application using the application factory pattern.
It registers blueprints and initializes extensions.
"""

import os
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from app.config import config_by_name
from app.extensions import db


def create_app(config_name=None):
    """
    Application factory pattern for creating Flask app.
    
    Args:
        config_name (str): Configuration name (development, testing, production)
        
    Returns:
        Flask: Configured Flask application
    """
    app = Flask(__name__)
    
    # Get configuration
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    config = config_by_name.get(config_name, config_by_name['default'])
    app.config.from_object(config)
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    CORS(app)
    
    # Register blueprints
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Register error handlers
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)
    
    return app
