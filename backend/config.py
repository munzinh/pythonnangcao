"""
Configuration module for Flask application.

This module handles application configuration including database settings,
secret keys, and environment-specific configurations.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Base configuration class.
    
    Attributes:
        SECRET_KEY (str): Secret key for Flask session
        SQLALCHEMY_DATABASE_URI (str): Database connection string
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): Disable SQLAlchemy modification tracking
    """
    
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'mysql+pymysql://todo_user:password@localhost/todo_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False
    # Tối ưu performance
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = False


class TestingConfig(Config):
    """Testing configuration."""
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URI', 'mysql+pymysql://todo_user:password@localhost/test_todo_db')


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False
    # Tối ưu performance cho production
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = False
    # Tối ưu database
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 20,
        'max_overflow': 30,
        'pool_recycle': 3600,
        'pool_timeout': 30
    }


config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
