# Ứng dụng To-Do List - Đồ án Python Nâng Cao

## Mô tả
Ứng dụng quản lý công việc (To-Do List) với giao diện Tkinter GUI và backend Flask REST API, sử dụng SQLite database.

## Yêu cầu hệ thống
- Python 3.8+
- SQLite3

## Cài đặt

1. Clone repository
2. Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

3. Tạo file `.env` từ `.env.example`:
```bash
cp .env.example .env
```

4. Khởi tạo database và dữ liệu demo:
```bash
python seed.py
```

## Chạy ứng dụng

### Backend API
```bash
python backend/app.py
```
API sẽ chạy tại: http://localhost:5000

### Frontend GUI
```bash
python frontend/gui.py
```

## Chạy Tests
```bash
pytest tests/
```

## Cấu trúc project
```
todo_project/
├── backend/          # Flask REST API
├── frontend/         # Tkinter GUI
├── tests/           # Unit tests
├── docs/            # Tài liệu, ERD, flowchart
├── seed.py          # Seed script
├── requirements.txt
├── .env.example
└── README.md
```

## API Endpoints
- GET /api/tasks - Lấy danh sách tasks
- POST /api/tasks - Tạo task mới
- PUT /api/tasks/<id> - Cập nhật task
- DELETE /api/tasks/<id> - Xóa task
- GET /api/tasks/search?q=<query> - Tìm kiếm tasks
- GET /api/tasks/export/csv - Export CSV
- GET /api/tasks/export/json - Export JSON

## Tính năng
- ✅ CRUD operations (Create, Read, Update, Delete)
- ✅ Đánh dấu hoàn thành task
- ✅ Tìm kiếm và lọc tasks
- ✅ Export dữ liệu (CSV/JSON)
- ✅ OOP design pattern
- ✅ Exception handling
- ✅ Unit tests với pytest

## TODO - Hoàn thiện thêm
- [ ] Thêm ERD vào docs/
- [ ] Thêm Flowchart vào docs/
- [ ] Chụp screenshots ứng dụng
- [ ] Viết báo cáo chi tiết
