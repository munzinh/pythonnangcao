# To-Do List Application - Python Project

## Overview
Ứng dụng quản lý công việc (To-Do List) với giao diện Tkinter GUI và backend Flask REST API, sử dụng SQLite database. Đây là đồ án môn Python Nâng Cao theo yêu cầu PPW.

## Current State
- ✅ Backend Flask API hoàn thành với CRUD endpoints
- ✅ Frontend Tkinter GUI hoàn thành với Treeview và các controls
- ✅ SQLite database với SQLAlchemy ORM
- ✅ Unit tests (16 tests passed)
- ✅ Seed script với sample data
- ✅ Export CSV/JSON functionality
- ✅ OOP design pattern
- ✅ Exception handling
- ✅ PEP8 compliant với docstrings

## Recent Changes (2025-10-03)
- Tạo toàn bộ skeleton code cho project
- Setup backend Flask API với SQLAlchemy models và routes
- Tạo frontend Tkinter GUI với Treeview
- Viết 16 unit tests với pytest (all passing)
- Tạo seed script với 8 sample tasks
- Fix test configuration issue với conftest.py
- Setup workflow để chạy backend API server

## Project Architecture

### Backend (Flask REST API)
- **backend/app.py**: Flask application entry point
- **backend/config.py**: Configuration classes (Development, Testing, Production)
- **backend/database.py**: SQLAlchemy database connection và session management
- **backend/models.py**: Task model và TaskManager class (OOP)
- **backend/routes.py**: API endpoints (CRUD, search, export)

### Frontend (Tkinter GUI)
- **frontend/gui.py**: Main GUI application với TodoApp class
- **frontend/api_client.py**: API client để communicate với backend

### Tests
- **tests/conftest.py**: Pytest fixtures và configuration
- **tests/test_api.py**: Unit tests cho tất cả API endpoints

### Database Schema
- **Task model**: id, title, description, completed, priority, created_at, updated_at

## Technical Stack
- **Backend**: Flask 3.0.0, SQLAlchemy 2.0.23
- **Frontend**: Tkinter (built-in)
- **Database**: SQLite
- **Testing**: pytest 7.4.3
- **API Communication**: requests 2.31.0

## Running the Application

### Backend API
```bash
DATABASE_URL=sqlite:///todo.db PYTHONPATH=/home/runner/workspace:$PYTHONPATH python backend/app.py
```
API runs on http://localhost:5000

### Frontend GUI
```bash
PYTHONPATH=/home/runner/workspace:$PYTHONPATH python frontend/gui.py
```

### Seed Database
```bash
DATABASE_URL=sqlite:///todo.db PYTHONPATH=/home/runner/workspace:$PYTHONPATH python seed.py
```

### Run Tests
```bash
DATABASE_URL=sqlite:///test_todo.db PYTHONPATH=/home/runner/workspace:$PYTHONPATH pytest tests/ -v
```

## API Endpoints
- GET /api/tasks - Lấy danh sách tasks
- POST /api/tasks - Tạo task mới
- GET /api/tasks/<id> - Lấy task theo ID
- PUT /api/tasks/<id> - Cập nhật task
- DELETE /api/tasks/<id> - Xóa task
- GET /api/tasks/search?q=<query> - Tìm kiếm tasks
- GET /api/tasks/export/csv - Export CSV
- GET /api/tasks/export/json - Export JSON

## User Preferences
- Language: Vietnamese
- Code style: PEP8 compliant
- Documentation: Full docstrings cho tất cả functions/classes
- OOP: Sử dụng classes cho encapsulation
- Error handling: Comprehensive try-except blocks

## TODO - Next Steps
- [ ] Thêm ERD diagram vào docs/
- [ ] Tạo Flowchart cho application flow
- [ ] Chụp screenshots của GUI
- [ ] Viết báo cáo chi tiết cho đồ án
- [ ] (Optional) Cải thiện UI với màu sắc và icons
- [ ] (Optional) Thêm authentication nếu cần

## Notes
- Project sử dụng SQLite thay vì MySQL do hạn chế môi trường Replit
- Code structure tuân thủ yêu cầu PPW (module/package organization)
- Workflow đã được setup để auto-run backend API
- PYTHONPATH cần được set để import modules work correctly
