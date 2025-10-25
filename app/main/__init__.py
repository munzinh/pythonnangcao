"""
Main Blueprint.

This module defines the main blueprint for web frontend routes.
"""

from flask import Blueprint

bp = Blueprint('main', __name__)

from app.main import routes
