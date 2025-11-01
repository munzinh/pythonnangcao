"""
File tạo app Flask theo dạng Factory Pattern.
Giúp app dễ mở rộng, dễ test, register các route và extension gọn gàng.
"""
import os
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from app.config import config_by_name
from app.extensions import db

def create_app(config_name=None):
    """Tạo & trả về app Flask đã đăng ký các route, middleware."""
    app = Flask(__name__)
    # Lấy cấu hình theo tên môi trường
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    config = config_by_name.get(config_name, config_by_name['default'])
    app.config.from_object(config)
    # Khởi tạo extension
    db.init_app(app)
    migrate = Migrate(app, db)
    CORS(app)
    # Đăng ký route cho app (chia theo blueprint)
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)
    return app
