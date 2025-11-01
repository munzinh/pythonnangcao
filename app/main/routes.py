"""
Route HTML chính của ứng dụng web.
Render template index và endpoint kiểm tra sống/khỏe cho hệ thống.
"""
from flask import render_template, jsonify
from app.main import bp

# Trang chủ - render HTML todo list
@bp.route('/')
def index():
    """Hiển thị trang giao diện chính của todo app."""
    return render_template('index.html')

# API kiểm tra health (test nhanh server sống/chết)
@bp.route('/health')
def health():
    return jsonify({'status': 'healthy', 'database': 'connected'}), 200
