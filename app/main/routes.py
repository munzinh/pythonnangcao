"""
Main routes for web frontend.

This module defines routes that render HTML templates.
"""

from flask import render_template, jsonify
from app.main import bp


@bp.route('/')
def index():
    """Render the main todo list page."""
    return render_template('index.html')


@bp.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'database': 'connected'
    }), 200
