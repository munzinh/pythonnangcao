"""
File chạy chính của ứng dụng Flask (entrypoint).
Chỉ sử dụng khi bạn muốn chạy demo/thử nghiệm trực tiếp.
"""
import os
from app import create_app

app = create_app()  # Gọi hàm factory để sinh ra app Flask

if __name__ == '__main__':
    # Lấy thông số môi trường (nếu muốn tuỳ chỉnh khi run)
    env = os.getenv('FLASK_ENV', 'development')
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', '5000'))

    # In ra console thông tin server
    print("=" * 60)
    print("TaskMaster - Todo List Application")
    print("=" * 60)
    print(f"Environment: {env}")
    print(f"Debug Mode: {debug}")
    print(f"Database: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print("=" * 60)
    print("Available Endpoints:")
    # Port sẽ được điều chỉnh tự động (5000 trong container, 5001 khi map từ Docker)
    print(f"  Web Interface: http://{host}:{port}/")
    print("  API Endpoints:")
    print("    - GET    /api/tasks")
    print("    - POST   /api/tasks")
    print("    - GET    /api/tasks/<id>")
    print("    - PUT    /api/tasks/<id>")
    print("    - DELETE /api/tasks/<id>")
    print("    - GET    /api/tasks/search?q=<query>")
    print("    - GET    /api/tasks/export/csv")
    print("    - GET    /api/tasks/export/json")
    print("=" * 60)
    print("Starting server...")
    print("=" * 60)

    app.run(host=host, port=port, debug=debug)
