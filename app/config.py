"""
File cấu hình chính cho Flask.
Khi dùng Docker: biến môi trường được set trong docker-compose.yml
Khi chạy manual: có thể dùng file .env (không bắt buộc)
"""
import os
from dotenv import load_dotenv
load_dotenv()  # Đọc .env nếu có (chỉ cần khi chạy manual, không dùng Docker)

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production') # Khoá bảo mật session
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///todo.db')   # Đường dẫn DB mặc định sqlite (dễ deploy demo)
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Không theo dõi object, tiết kiệm tài nguyên
    JSON_AS_ASCII = False                   # Hỗ trợ hiển thị Unicode

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False
    JSON_SORT_KEYS = False  # Để nguyên thứ tự field trả về JSON
    JSONIFY_PRETTYPRINT_REGULAR = False  # API trả về gọn nhẹ

class TestingConfig(Config):
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URI', 'sqlite:///test_todo.db') # DB test riêng
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = False
    SQLALCHEMY_ENGINE_OPTIONS = {  # Tối ưu hoá pool kết nối DB
        'pool_size': 20, 'max_overflow': 30, 'pool_recycle': 3600, 'pool_timeout': 30
    }

config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
