"""
Nơi khởi tạo các extension Flask dùng chung (tránh lỗi import vòng).
Hiện dùng SQLAlchemy cho ORM quản lý CSDL.
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Object này sẽ được app import để mọi file khác dùng chung
