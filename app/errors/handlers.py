"""
Error handlers for the application.

This module defines custom error handlers for different HTTP status codes.
"""

from flask import render_template, jsonify, request
from app.errors import bp


@bp.app_errorhandler(404)
def not_found_error(error):
    """Handle 404 errors."""
    if request.path.startswith('/api/'):
        return jsonify({
            'success': False,
            'error': 'API endpoint not found'
        }), 404
    return render_template('errors/404.html'), 404


@bp.app_errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    if request.path.startswith('/api/'):
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500
    return render_template('errors/500.html'), 500
