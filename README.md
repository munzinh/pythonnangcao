# TaskMaster - Todo List Application

A modern, professional Flask web application for managing your tasks with a clean, responsive interface built with Bootstrap 5.

## 🚀 Quick Start với Docker (Khuyến nghị)

### Yêu cầu
- Docker Desktop (Windows/Mac) hoặc Docker Engine + Docker Compose (Linux)
- Git

### Cài đặt và chạy

```bash
# 1. Clone repository
git clone <repository-url>
cd TaskMaster

# 2. Khởi động ứng dụng với Docker Compose
docker-compose up --build

# Hoặc chạy ở background
docker-compose up -d --build
```

### Truy cập ứng dụng

Sau khi containers khởi động thành công, truy cập:

- **Web Interface**: http://localhost:5001
- **API Base**: http://localhost:5001/api/

### Thông tin Database (Docker)

- **Host**: localhost:3307
- **Username**: `todo_user`
- **Password**: `todo_password`
- **Database**: `taskmaster_db`

### Các lệnh Docker hữu ích

```bash
# Xem logs
docker-compose logs -f web

# Dừng services
docker-compose down

# Dừng và xóa volumes (mất dữ liệu database)
docker-compose down -v

# Rebuild lại image
docker-compose build --no-cache

# Truy cập vào container MySQL
docker-compose exec db mysql -u todo_user -ptodo_password taskmaster_db

# Truy cập vào container Flask
docker-compose exec web bash

# Chạy migrations thủ công (nếu cần)
docker-compose exec web flask db upgrade

# Restart services
docker-compose restart
```

### Troubleshooting Docker

**Lỗi port đã được sử dụng:**
- Ports mặc định: Web = 5001, MySQL = 3307
- Nếu cần đổi, sửa trong `docker-compose.yml`:
  - Web: `"5002:5000"` (port 5002 trên máy host → 5000 trong container)
  - MySQL: `"3308:3306"`

**Reset hoàn toàn:**
```bash
docker-compose down -v
docker-compose up --build
```

**Lỗi kết nối database:**
```bash
# Kiểm tra MySQL container
docker-compose ps
docker-compose logs db
```

---

## 🛠️ Cài đặt thủ công (Không dùng Docker - Tùy chọn)

> **Lưu ý:** Đồ án này được tối ưu cho Docker. Nếu muốn chạy manual, bạn cần:
> - Python 3.8+, pip
> - MySQL (nếu dùng MySQL) hoặc SQLite
> - Tạo file `.env` với `DATABASE_URI` và `SECRET_KEY`

```bash
# Cài đặt dependencies
pip install -r requirements.txt

# Tạo file .env (nếu chưa có)
# DATABASE_URI=sqlite:///todo.db  (hoặc MySQL URI)
# SECRET_KEY=your-secret-key

# Chạy migrations và ứng dụng
flask db upgrade
python run.py
```

## 📚 API Documentation

### Task Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tasks` | Get all tasks |
| POST | `/api/tasks` | Create a new task |
| GET | `/api/tasks/<id>` | Get a specific task |
| PUT | `/api/tasks/<id>` | Update a task |
| DELETE | `/api/tasks/<id>` | Delete a task |
| GET | `/api/tasks/search?q=<query>` | Search tasks |
| GET | `/api/tasks/export/csv` | Export tasks as CSV |
| GET | `/api/tasks/export/json` | Export tasks as JSON |

### Request/Response Examples

#### Create a Task
```bash
curl -X POST http://localhost:5001/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project",
    "description": "Finish the TaskMaster application",
    "priority": "High"
  }'
```

#### Get All Tasks
```bash
curl http://localhost:5001/api/tasks
```

#### Update a Task
```bash
curl -X PUT http://localhost:5001/api/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{
    "completed": true
  }'
```

## 🎨 Features

- **Modern Web Interface**: Clean, responsive design with Bootstrap 5
- **Full CRUD Operations**: Create, read, update, and delete tasks
- **Task Management**: Mark tasks as completed, set priorities, add descriptions
- **Search & Filter**: Search tasks by title/description, filter by completion status
- **Export Functionality**: Export tasks to CSV or JSON format
- **RESTful API**: Complete API endpoints for all operations
- **Database Support**: MySQL (Docker) or SQLite (manual setup)
- **Professional Structure**: Organized codebase following Flask best practices

## 📁 Project Structure

```
TaskMaster/
├── app/                    # Main application package
│   ├── api/               # API blueprint (REST endpoints)
│   │   ├── __init__.py
│   │   └── routes.py      # API routes
│   ├── main/              # Web frontend blueprint
│   │   ├── __init__.py
│   │   └── routes.py      # Web routes
│   ├── errors/            # Error handlers
│   │   ├── __init__.py
│   │   └── handlers.py    # Error handling
│   ├── static/            # Static files
│   │   ├── css/
│   │   │   └── main.css   # Custom styles
│   │   └── js/
│   │       └── main.js    # Frontend JavaScript
│   ├── templates/         # HTML templates
│   │   ├── base.html      # Base template
│   │   ├── index.html     # Main page
│   │   └── errors/        # Error pages
│   ├── __init__.py        # Application factory
│   ├── config.py          # Configuration
│   ├── extensions.py      # Flask extensions
│   └── models.py          # Database models
├── migrations/            # Database migrations (Flask-Migrate)
├── Dockerfile            # Docker image definition
├── docker-compose.yml    # Docker Compose configuration
├── init.sql              # MySQL initialization script
├── run.py                # Application entry point
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `FLASK_ENV` | `development` | Flask environment |
| `FLASK_DEBUG` | `True` | Debug mode |
| `SECRET_KEY` | `dev-secret-key...` | Flask secret key |
| `DATABASE_URI` | `sqlite:///todo.db` | Database connection string |

### Configuration Classes

The application supports multiple configuration environments:

- **Development**: Debug enabled, SQLite database
- **Testing**: Test database, debug disabled
- **Production**: Optimized settings, production database

## 🗄️ Database Configuration

### Docker (Khuyến nghị)

MySQL được cấu hình tự động trong Docker:
- **Host**: `db` (tên service trong docker-compose)
- **Port**: `3306` (trong container)
- **Database**: `taskmaster_db`
- **User**: `todo_user`
- **Password**: `todo_password`

Không cần cấu hình thêm, tất cả đã được set trong `docker-compose.yml`.

### Manual Setup (Tùy chọn)

Nếu chạy không dùng Docker, có thể dùng SQLite (mặc định) hoặc MySQL. Xem phần "Cài đặt thủ công" ở trên.

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_api.py
```

## 📦 Deployment

### Docker Deployment (Khuyến nghị)

```bash
# Build và chạy production
docker-compose up -d --build

# Xem logs
docker-compose logs -f

# Dừng
docker-compose down
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/your-repo/issues) page
2. Create a new issue with detailed information
3. Contact the development team

## 🎯 Roadmap

- [ ] User authentication and authorization
- [ ] Task categories and tags
- [ ] Due dates and reminders
- [ ] File attachments
- [ ] Team collaboration features
- [ ] Mobile app
- [ ] Advanced reporting and analytics

---

**Built with ❤️ using Flask, Bootstrap, Docker, and modern web technologies.**
