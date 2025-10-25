"""
Error Handlers Blueprint.

This module defines error handlers for the application.
"""

from flask import Blueprint

bp = Blueprint('errors', __name__)

from app.errors import handlers
