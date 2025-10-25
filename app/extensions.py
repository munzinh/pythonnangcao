"""
Flask Extensions.

This module initializes Flask extensions to avoid circular imports.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
