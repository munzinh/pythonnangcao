"""
Pytest configuration and fixtures for testing.

This module provides shared fixtures and test configuration
for the test suite.
"""

import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app
from backend.database import Base, engine, init_db


@pytest.fixture(scope='session')
def app():
    """
    Create Flask app for testing.
    
    Returns:
        Flask: Test Flask application
    """
    test_app = create_app('testing')
    
    with test_app.app_context():
        init_db(test_app)
        Base.metadata.create_all(bind=engine)
    
    yield test_app
    
    with test_app.app_context():
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope='function')
def client(app):
    """
    Create test client.
    
    Args:
        app: Flask test application
        
    Returns:
        FlaskClient: Test client for making requests
    """
    return app.test_client()


@pytest.fixture(scope='function')
def init_database(app):
    """
    Initialize and clean database for each test.
    
    Args:
        app: Flask test application
    """
    with app.app_context():
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
    
    yield
    
    with app.app_context():
        Base.metadata.drop_all(bind=engine)
