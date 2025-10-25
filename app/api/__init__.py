"""
API Blueprint.

This module defines the API blueprint for REST endpoints.
"""

from flask import Blueprint

bp = Blueprint('api', __name__)

from app.api import routes
