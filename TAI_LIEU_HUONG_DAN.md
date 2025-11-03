# 📚 TÀI LIỆU HƯỚNG DẪN CHI TIẾT - TASKMASTER

## MỤC LỤC

1. [TỔNG QUAN DỰ ÁN](#1-tổng-quan-dự-án)
2. [KIẾN TRÚC HỆ THỐNG](#2-kiến-trúc-hệ-thống)
3. [LUỒNG HOẠT ĐỘNG CHI TIẾT](#3-luồng-hoạt-động-chi-tiết)
4. [CÁC THÀNH PHẦN CHÍNH](#4-các-thành-phần-chính)
5. [SƠ ĐỒ LUỒNG DỮ LIỆU](#5-sơ-đồ-luồng-dữ-liệu)
6. [CƠ SỞ DỮ LIỆU](#6-cơ-sở-dữ-liệu)
7. [API DOCUMENTATION](#7-api-documentation)
8. [HƯỚNG DẪN CÀI ĐẶT](#8-hướng-dẫn-cài-đặt)
9. [DEMO VÀ THUYẾT TRÌNH](#9-demo-và-thuyết-trình)

---

## 1. TỔNG QUAN DỰ ÁN

### 1.1. Giới thiệu

**TaskMaster** là một ứng dụng quản lý công việc (To-Do List) được xây dựng bằng:

- **Backend**: Flask (Python) - Web framework nhẹ và linh hoạt
- **Frontend**: HTML, CSS (Bootstrap 5), JavaScript (Vanilla JS)
- **Database**: MySQL 8.0 (qua Docker) hoặc SQLite
- **ORM**: SQLAlchemy - Quản lý database dễ dàng
- **Containerization**: Docker & Docker Compose

### 1.2. Tính năng chính

1. ✅ **CRUD đầy đủ**: Tạo, đọc, cập nhật, xóa task
2. 🔍 **Tìm kiếm**: Tìm kiếm task theo tiêu đề/mô tả
3. 🎯 **Lọc dữ liệu**: Lọc theo trạng thái hoàn thành
4. 📊 **Xuất dữ liệu**: Export CSV và JSON
5. 🎨 **Giao diện đẹp**: Responsive design với Bootstrap 5
6. 🔌 **RESTful API**: API đầy đủ cho mọi thao tác
7. 🐳 **Docker Ready**: Chạy ngay với Docker Compose

---

## 2. KIẾN TRÚC HỆ THỐNG

### 2.1. Sơ đồ kiến trúc tổng quan

```
┌─────────────────────────────────────────────────────────┐
│                    CLIENT (Browser)                     │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Frontend: HTML + Bootstrap 5 + JavaScript        │  │
│  │  - Giao diện người dùng                           │  │
│  │  - Xử lý AJAX requests                            │  │
│  │  - Hiển thị dữ liệu                               │  │
│  └──────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP/HTTPS
                     │ (RESTful API)
                     ▼
┌─────────────────────────────────────────────────────────┐
│              FLASK APPLICATION SERVER                   │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Blueprint: Main Routes (Web Interface)          │  │
│  │  Blueprint: API Routes (REST API)               │  │
│  │  Blueprint: Error Handlers                       │  │
│  └──────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Business Logic Layer: TaskManager                │  │
│  │  - create_task()                                 │  │
│  │  - get_all_tasks()                               │  │
│  │  - update_task()                                 │  │
│  │  - delete_task()                                 │  │
│  │  - search_tasks()                                │  │
│  └──────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Data Access Layer: SQLAlchemy ORM                │  │
│  │  - Task Model                                    │  │
│  │  - Database Queries                              │  │
│  └──────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────┘
                     │ SQL Queries
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  MYSQL DATABASE                        │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Table: tasks                                    │  │
│  │  - id (PK)                                       │  │
│  │  - title                                         │  │
│  │  - description                                   │  │
│  │  - completed                                     │  │
│  │  - priority                                      │  │
│  │  - created_at                                    │  │
│  │  - updated_at                                    │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### 2.2. Cấu trúc thư mục

```
TaskMaster/
├── app/                         # Package chính của ứng dụng
│   ├── __init__.py              # Application Factory Pattern
│   ├── config.py                # Cấu hình ứng dụng
│   ├── extensions.py            # Flask extensions (db, migrate)
│   ├── models.py                # Database models (Task, TaskManager)
│   │
│   ├── api/                     # API Blueprint
│   │   ├── __init__.py
│   │   └── routes.py            # API endpoints (REST)
│   │
│   ├── main/                    # Main Blueprint (Web UI)
│   │   ├── __init__.py
│   │   └── routes.py            # Web routes (HTML)
│   │
│   ├── errors/                  # Error Handling Blueprint
│   │   ├── __init__.py
│   │   └── handlers.py          # Error handlers (404, 500)
│   │
│   ├── static/                  # Static files
│   │   ├── css/
│   │   │   └── main.css         # Custom styles
│   │   └── js/
│   │       └── main.js          # Frontend JavaScript
│   │
│   └── templates/               # HTML templates
│       ├── base.html            # Base template
│       ├── index.html           # Main page
│       └── errors/
│           ├── 404.html
│           └── 500.html
│
├── migrations/                  # Database migrations
│   ├── versions/                # Migration files
│   └── ...
│
├── Dockerfile                   # Docker image definition
├── docker-compose.yml           # Docker Compose configuration
├── init.sql                     # MySQL initialization script
├── requirements.txt            # Python dependencies
├── run.py                      # Application entry point
└── README.md                   # Documentation
```

### 2.3. Design Patterns sử dụng

1. **Application Factory Pattern** (`app/__init__.py`)
   - Tạo ứng dụng Flask một cách linh hoạt
   - Dễ dàng test và cấu hình

2. **Blueprint Pattern** (Flask Blueprints)
   - Tách biệt routes thành các module
   - Dễ quản lý và mở rộng

3. **ORM Pattern** (SQLAlchemy)
   - Abstraction layer cho database
   - Không cần viết SQL thủ công

4. **Repository Pattern** (TaskManager)
   - Tách biệt business logic và data access
   - Dễ test và maintain

---

## 3. LUỒNG HOẠT ĐỘNG CHI TIẾT

### 3.1. Luồng khởi động ứng dụng

```
1. Người dùng chạy: docker-compose up --build
   │
   ├─► Docker Compose đọc docker-compose.yml
   │
   ├─► Khởi động MySQL Container
   │   ├─► Chạy init.sql (tạo DB, user, permissions)
   │   └─► Đợi MySQL ready (healthcheck)
   │
   └─► Khởi động Flask Container
       ├─► Build Docker image từ Dockerfile
       ├─► Cài đặt dependencies từ requirements.txt
       ├─► Copy source code vào container
       ├─► Chạy: flask db upgrade (migrations)
       └─► Chạy: python run.py
           │
           └─► create_app() được gọi
               ├─► Load config từ config.py
               ├─► Khởi tạo Flask app
               ├─► Khởi tạo SQLAlchemy (db)
               ├─► Khởi tạo Flask-Migrate
               ├─► Đăng ký Blueprints:
               │   ├─► Main Blueprint (/)
               │   ├─► API Blueprint (/api)
               │   └─► Errors Blueprint
               └─► Server chạy trên port 5000
```

### 3.2. Luồng xử lý request (Request Flow)

#### 3.2.1. Luồng xem danh sách task (GET /api/tasks)

```
[Browser] 
  │
  │ User click "Load Tasks" hoặc trang tự động load
  │
  ▼
[JavaScript - main.js]
  │
  │ fetch('/api/tasks', { method: 'GET' })
  │
  ▼
[HTTP Request]
  │ GET http://localhost:5001/api/tasks
  │
  ▼
[Flask Application]
  │
  │ Route matching: @bp.route('/tasks', methods=['GET'])
  │ Blueprint: api/routes.py
  │
  ▼
[API Handler - get_tasks()]
  │
  │ 1. Lấy query parameter: completed (optional)
  │ 2. Gọi TaskManager.get_all_tasks(completed)
  │
  ▼
[TaskManager.get_all_tasks()]
  │
  │ 1. Build query: Task.query
  │ 2. Filter by completed (nếu có)
  │ 3. Order by created_at DESC
  │ 4. Execute query: .all()
  │ 5. Convert to dict: [task.to_dict() for task in tasks]
  │
  ▼
[SQLAlchemy ORM]
  │
  │ Generate SQL: SELECT * FROM tasks WHERE ... ORDER BY created_at DESC
  │
  ▼
[MySQL Database]
  │
  │ Execute query, return rows
  │
  ▼
[TaskManager]
  │
  │ Convert database rows → Python dicts
  │ Return: [{'id': 1, 'title': '...', ...}, ...]
  │
  ▼
[API Handler]
  │
  │ Wrap in response:
  │ jsonify({
  │   'success': True,
  │   'data': tasks,
  │   'count': len(tasks)
  │ })
  │
  ▼
[HTTP Response]
  │ Status: 200 OK
  │ Content-Type: application/json
  │ Body: {"success": true, "data": [...], "count": 5}
  │
  ▼
[JavaScript]
  │
  │ Parse JSON response
  │ Update DOM: render tasks to table
  │
  ▼
[Browser]
  │
  │ Hiển thị danh sách task trên màn hình
```

#### 3.2.2. Luồng tạo task mới (POST /api/tasks)

```
[Browser]
  │
  │ User điền form và click "Add Task"
  │
  ▼
[JavaScript]
  │
  │ Collect form data:
  │ { title: "...", description: "...", priority: "High" }
  │
  │ fetch('/api/tasks', {
  │   method: 'POST',
  │   headers: { 'Content-Type': 'application/json' },
  │   body: JSON.stringify(data)
  │ })
  │
  ▼
[HTTP Request]
  │ POST http://localhost:5001/api/tasks
  │ Body: {"title": "...", "description": "...", "priority": "High"}
  │
  ▼
[Flask Application]
  │
  │ Route: @bp.route('/tasks', methods=['POST'])
  │
  ▼
[API Handler - create_task()]
  │
  │ 1. Parse JSON: request.get_json()
  │ 2. Validate: Kiểm tra 'title' có tồn tại
  │ 3. Gọi TaskManager.create_task(...)
  │
  ▼
[TaskManager.create_task()]
  │
  │ 1. Validate: title không được rỗng
  │ 2. Tạo Task object:
  │    task = Task(
  │      title=title.strip(),
  │      description=description,
  │      priority=priority
  │    )
  │ 3. db.session.add(task)
  │ 4. db.session.commit()
  │
  ▼
[SQLAlchemy]
  │
  │ Generate SQL: INSERT INTO tasks (title, description, ...) VALUES (...)
  │
  ▼
[MySQL Database]
  │
  │ Execute INSERT, return new task ID
  │
  ▼
[TaskManager]
  │
  │ task.to_dict() → Convert to dict
  │ Return: {'id': 5, 'title': '...', ...}
  │
  ▼
[API Handler]
  │
  │ jsonify({
  │   'success': True,
  │   'data': task,
  │   'message': 'Task created successfully'
  │ })
  │ Status: 201 Created
  │
  ▼
[JavaScript]
  │
  │ Success → Refresh task list
  │ Clear form
  │ Show success message
```

#### 3.2.3. Luồng cập nhật task (PUT /api/tasks/<id>)

```
[Browser]
  │ User click "Edit" → Modal hiện ra → Điền form → Click "Save"
  │
  ▼
[JavaScript]
  │
  │ fetch(`/api/tasks/${taskId}`, {
  │   method: 'PUT',
  │   body: JSON.stringify({ title: '...', completed: true })
  │ })
  │
  ▼
[API Handler - update_task(task_id)]
  │
  │ 1. Parse JSON body
  │ 2. Gọi TaskManager.update_task(task_id, **data)
  │
  ▼
[TaskManager.update_task()]
  │
  │ 1. Query: task = Task.query.filter(Task.id == task_id).first()
  │ 2. Update fields từ kwargs
  │ 3. task.updated_at = datetime.utcnow()
  │ 4. db.session.commit()
  │
  ▼
[Database]
  │ UPDATE tasks SET title=..., updated_at=... WHERE id=...
  │
  ▼
[Response]
  │ Status: 200 OK
  │ Body: {"success": true, "data": {...}, "message": "Task updated"}
  │
  ▼
[Browser]
  │ Refresh task list với data mới
```

#### 3.2.4. Luồng xóa task (DELETE /api/tasks/<id>)

```
[Browser]
  │ User click "Delete" → Confirm → OK
  │
  ▼
[JavaScript]
  │
  │ fetch(`/api/tasks/${taskId}`, { method: 'DELETE' })
  │
  ▼
[API Handler - delete_task(task_id)]
  │
  │ TaskManager.delete_task(task_id)
  │
  ▼
[TaskManager.delete_task()]
  │
  │ 1. Query: task = Task.query.filter(Task.id == task_id).first()
  │ 2. db.session.delete(task)
  │ 3. db.session.commit()
  │
  ▼
[Database]
  │ DELETE FROM tasks WHERE id = ...
  │
  ▼
[Response]
  │ Status: 200 OK
  │ Body: {"success": true, "message": "Task deleted"}
  │
  ▼
[Browser]
  │ Remove task from UI
```

#### 3.2.5. Luồng tìm kiếm (GET /api/tasks/search?q=...)

```
[Browser]
  │ User nhập text vào search box
  │
  ▼
[JavaScript]
  │
  │ Debounce → Sau 300ms không gõ nữa thì gửi request
  │ fetch(`/api/tasks/search?q=${searchText}`)
  │
  ▼
[API Handler - search_tasks()]
  │
  │ query = request.args.get('q')
  │ TaskManager.search_tasks(query)
  │
  ▼
[TaskManager.search_tasks()]
  │
  │ search_pattern = f"%{query}%"
  │ Task.query.filter(
  │   (Task.title.like(search_pattern)) |
  │   (Task.description.like(search_pattern))
  │ ).all()
  │
  ▼
[Database]
  │ SELECT * FROM tasks 
  │ WHERE title LIKE '%query%' OR description LIKE '%query%'
  │
  ▼
[Response]
  │ Status: 200 OK
  │ Body: {"success": true, "data": [...], "count": 3, "query": "..."}
  │
  ▼
[Browser]
  │ Hiển thị kết quả tìm kiếm
```

---

## 4. CÁC THÀNH PHẦN CHÍNH

### 4.1. Application Factory (`app/__init__.py`)

**Mục đích**: Tạo Flask application một cách linh hoạt, dễ test và cấu hình.

**Luồng hoạt động**:

```python
def create_app(config_name=None):
    # 1. Tạo Flask app instance
    app = Flask(__name__)
    
    # 2. Load configuration
    config = config_by_name.get(config_name, config_by_name['default'])
    app.config.from_object(config)
    
    # 3. Khởi tạo extensions
    db.init_app(app)           # SQLAlchemy
    migrate = Migrate(app, db) # Flask-Migrate
    CORS(app)                  # Cross-Origin Resource Sharing
    
    # 4. Đăng ký Blueprints
    app.register_blueprint(main_bp)      # Web UI routes
    app.register_blueprint(api_bp, url_prefix='/api')  # API routes
    app.register_blueprint(errors_bp)    # Error handlers
    
    return app
```

**Tại sao dùng Factory Pattern?**
- Dễ test: Có thể tạo nhiều app instances với config khác nhau
- Linh hoạt: Có thể chạy app ở nhiều môi trường (dev, test, production)
- Clean code: Tách biệt việc tạo app và chạy app

### 4.2. Models (`app/models.py`)

#### 4.2.1. Task Model

**Mục đích**: Đại diện cho một task trong database (ORM Model).

```python
class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    completed = db.Column(db.Boolean, default=False, nullable=False, index=True)
    priority = db.Column(db.String(20), default='Medium', index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, 
                           onupdate=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        """Convert Task object to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'priority': self.priority,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
```

**Giải thích các trường**:
- `id`: Primary key, tự động tăng
- `title`: Tiêu đề task (bắt buộc, có index để tìm kiếm nhanh)
- `description`: Mô tả chi tiết (không bắt buộc)
- `completed`: Trạng thái hoàn thành (True/False, có index)
- `priority`: Mức độ ưu tiên (High/Medium/Low, có index)
- `created_at`: Thời gian tạo (tự động set khi tạo mới)
- `updated_at`: Thời gian cập nhật cuối (tự động update khi thay đổi)

#### 4.2.2. TaskManager Class

**Mục đích**: Business Logic Layer - Xử lý tất cả thao tác với Task.

**Các phương thức**:

1. **create_task(title, description, priority)**
   - Validate input
   - Tạo Task object
   - Lưu vào database
   - Return dict

2. **get_all_tasks(completed=None)**
   - Query tất cả tasks
   - Filter theo completed (nếu có)
   - Sort theo created_at DESC
   - Return list of dicts

3. **get_task_by_id(task_id)**
   - Query task theo ID
   - Return dict hoặc None

4. **update_task(task_id, **kwargs)**
   - Query task theo ID
   - Update các field được truyền vào
   - Tự động update `updated_at`
   - Commit changes
   - Return dict

5. **delete_task(task_id)**
   - Query task theo ID
   - Xóa khỏi database
   - Return True/False

6. **search_tasks(query)**
   - Tìm kiếm trong title và description
   - Sử dụng SQL LIKE với pattern `%query%`
   - Return list of dicts

### 4.3. API Routes (`app/api/routes.py`)

**Mục đích**: Xử lý các HTTP requests và trả về JSON responses.

**Các endpoints**:

| Method | Endpoint | Handler Function | Mô tả |
|--------|----------|------------------|-------|
| GET | `/api/tasks` | `get_tasks()` | Lấy danh sách tất cả tasks |
| GET | `/api/tasks/<id>` | `get_task(task_id)` | Lấy 1 task theo ID |
| POST | `/api/tasks` | `create_task()` | Tạo task mới |
| PUT | `/api/tasks/<id>` | `update_task(task_id)` | Cập nhật task |
| DELETE | `/api/tasks/<id>` | `delete_task(task_id)` | Xóa task |
| GET | `/api/tasks/search?q=<query>` | `search_tasks()` | Tìm kiếm tasks |
| GET | `/api/tasks/export/csv` | `export_csv()` | Export CSV |
| GET | `/api/tasks/export/json` | `export_json()` | Export JSON |

**Cấu trúc Response chuẩn**:

```json
{
  "success": true/false,
  "data": {...} hoặc [...],
  "message": "..." (optional),
  "error": "..." (nếu có lỗi),
  "count": 5 (cho list endpoints)
}
```

### 4.4. Frontend (`app/static/js/main.js`)

**Mục đích**: Xử lý tương tác người dùng và giao tiếp với API.

**Các chức năng chính**:

1. **loadTasks()**
   - Gọi GET /api/tasks
   - Render tasks vào bảng HTML
   - Update UI

2. **addTask()**
   - Lấy data từ form
   - Gọi POST /api/tasks
   - Refresh list nếu success

3. **updateTask(id)**
   - Hiển thị modal với data hiện tại
   - Gọi PUT /api/tasks/<id>
   - Refresh list

4. **deleteTask(id)**
   - Confirm với user
   - Gọi DELETE /api/tasks/<id>
   - Remove từ UI

5. **searchTasks(query)**
   - Debounce (chờ 300ms)
   - Gọi GET /api/tasks/search?q=...
   - Update UI với kết quả

6. **exportData(format)**
   - format = 'csv' hoặc 'json'
   - Gọi GET /api/tasks/export/csv hoặc /json
   - Trigger download

### 4.5. Configuration (`app/config.py`)

**Mục đích**: Quản lý cấu hình cho các môi trường khác nhau.

**Các config classes**:

1. **Config** (Base class)
   - SECRET_KEY
   - SQLALCHEMY_DATABASE_URI
   - SQLALCHEMY_TRACK_MODIFICATIONS

2. **DevelopmentConfig**
   - DEBUG = True
   - SQLite database mặc định

3. **TestingConfig**
   - DEBUG = False
   - TESTING = True
   - Test database riêng

4. **ProductionConfig**
   - DEBUG = False
   - Database connection pooling
   - Optimized settings

---

## 5. SƠ ĐỒ LUỒNG DỮ LIỆU

### 5.1. Luồng dữ liệu tổng quan

```
┌──────────────┐
│   Browser    │
│  (Frontend)  │
└──────┬───────┘
       │
       │ HTTP Request (JSON)
       │
       ▼
┌─────────────────────────────────┐
│   Flask Application             │
│                                 │
│  ┌──────────────────────────┐  │
│  │  API Routes Handler      │  │
│  │  - Parse request         │  │
│  │  - Validate data         │  │
│  └──────────┬───────────────┘  │
│             │                   │
│             ▼                   │
│  ┌──────────────────────────┐  │
│  │  TaskManager             │  │
│  │  - Business logic        │  │
│  │  - Data validation      │  │
│  └──────────┬───────────────┘  │
│             │                   │
│             ▼                   │
│  ┌──────────────────────────┐  │
│  │  SQLAlchemy ORM          │  │
│  │  - Convert to SQL       │  │
│  └──────────┬───────────────┘  │
└─────────────┼──────────────────┘
              │
              │ SQL Query
              │
              ▼
┌─────────────────────────────────┐
│      MySQL Database             │
│                                 │
│  ┌──────────────────────────┐  │
│  │  Table: tasks           │  │
│  │  - Execute SQL          │  │
│  │  - Return results       │  │
│  └──────────┬───────────────┘  │
└─────────────┼──────────────────┘
              │
              │ Database Rows
              │
              ▼
┌─────────────────────────────────┐
│  SQLAlchemy ORM                 │
│  - Convert rows to Python objs  │
└──────────┬──────────────────────┘
            │
            │ Task objects
            │
            ▼
┌─────────────────────────────────┐
│  TaskManager                     │
│  - Convert to dict (.to_dict()) │
└──────────┬──────────────────────┘
            │
            │ Python dicts
            │
            ▼
┌─────────────────────────────────┐
│  API Handler                     │
│  - Wrap in JSON response        │
└──────────┬──────────────────────┘
            │
            │ HTTP Response (JSON)
            │
            ▼
┌─────────────────────────────────┐
│  Browser                         │
│  - Parse JSON                    │
│  - Update UI                     │
└─────────────────────────────────┘
```

### 5.2. Luồng tạo task (Chi tiết)

```
[User Input]
  │
  │ Form: {title: "Task 1", description: "...", priority: "High"}
  │
  ▼
[Frontend Validation]
  │ Kiểm tra title không rỗng
  │
  ▼
[HTTP POST /api/tasks]
  │ Content-Type: application/json
  │ Body: {"title": "Task 1", "description": "...", "priority": "High"}
  │
  ▼
[Flask Route Handler]
  │ @bp.route('/tasks', methods=['POST'])
  │ def create_task():
  │   data = request.get_json()
  │
  ▼
[API Validation]
  │ if 'title' not in data:
  │   return error 400
  │
  ▼
[TaskManager.create_task()]
  │ task = Task(title=..., description=..., priority=...)
  │ db.session.add(task)
  │
  ▼
[SQLAlchemy ORM]
  │ INSERT INTO tasks (title, description, priority, completed, created_at, updated_at)
  │ VALUES ('Task 1', '...', 'High', 0, NOW(), NOW())
  │
  ▼
[MySQL Database]
  │ Execute INSERT
  │ Return: Auto-generated ID = 5
  │
  ▼
[TaskManager]
  │ db.session.commit()
  │ task.to_dict()
  │ → {'id': 5, 'title': 'Task 1', ...}
  │
  ▼
[API Response]
  │ HTTP 201 Created
  │ {
  │   "success": true,
  │   "data": {"id": 5, "title": "Task 1", ...},
  │   "message": "Task created successfully"
  │ }
  │
  ▼
[Frontend]
  │ Parse response
  │ Refresh task list
  │ Show success notification
```

---

## 6. CƠ SỞ DỮ LIỆU

### 6.1. Database Schema

**Table: tasks**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | ID duy nhất của task |
| title | VARCHAR(200) | NOT NULL, INDEXED | Tiêu đề task |
| description | TEXT | NULL | Mô tả chi tiết |
| completed | BOOLEAN | NOT NULL, DEFAULT FALSE, INDEXED | Trạng thái hoàn thành |
| priority | VARCHAR(20) | DEFAULT 'Medium', INDEXED | Mức độ ưu tiên |
| created_at | DATETIME | NOT NULL, INDEXED | Thời gian tạo |
| updated_at | DATETIME | NOT NULL | Thời gian cập nhật cuối |

### 6.2. ERD (Entity Relationship Diagram)

```
┌─────────────────────┐
│       TASKS         │
├─────────────────────┤
│ id (PK)             │
│ title               │
│ description         │
│ completed           │
│ priority            │
│ created_at          │
│ updated_at          │
└─────────────────────┘
```

*(Đơn giản vì chỉ có 1 bảng)*

### 6.3. SQL Queries mẫu

#### CREATE TABLE (Migration tự động tạo)

```sql
CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    priority VARCHAR(20) DEFAULT 'Medium',
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    INDEX idx_title (title),
    INDEX idx_completed (completed),
    INDEX idx_priority (priority),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

#### SELECT - Lấy tất cả tasks

```sql
SELECT * FROM tasks ORDER BY created_at DESC;
```

#### SELECT - Lọc theo completed

```sql
SELECT * FROM tasks 
WHERE completed = TRUE 
ORDER BY created_at DESC;
```

#### SELECT - Tìm kiếm

```sql
SELECT * FROM tasks 
WHERE title LIKE '%keyword%' 
   OR description LIKE '%keyword%'
ORDER BY created_at DESC;
```

#### INSERT - Tạo task mới

```sql
INSERT INTO tasks (title, description, priority, completed, created_at, updated_at)
VALUES ('New Task', 'Description here', 'High', FALSE, NOW(), NOW());
```

#### UPDATE - Cập nhật task

```sql
UPDATE tasks 
SET title = 'Updated Title',
    completed = TRUE,
    updated_at = NOW()
WHERE id = 1;
```

#### DELETE - Xóa task

```sql
DELETE FROM tasks WHERE id = 1;
```

---

## 7. API DOCUMENTATION

### 7.1. Base URL

```
http://localhost:5001/api
```

### 7.2. Endpoints Chi Tiết

#### 7.2.1. GET /api/tasks

**Mô tả**: Lấy danh sách tất cả tasks.

**Query Parameters**:
- `completed` (optional): `true` hoặc `false` - Lọc theo trạng thái

**Ví dụ Request**:
```bash
# Lấy tất cả
GET /api/tasks

# Chỉ lấy tasks đã hoàn thành
GET /api/tasks?completed=true

# Chỉ lấy tasks chưa hoàn thành
GET /api/tasks?completed=false
```

**Response (200 OK)**:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "title": "Task 1",
      "description": "Description here",
      "completed": false,
      "priority": "High",
      "created_at": "2025-11-01T10:00:00",
      "updated_at": "2025-11-01T10:00:00"
    },
    ...
  ],
  "count": 5
}
```

---

#### 7.2.2. GET /api/tasks/<id>

**Mô tả**: Lấy thông tin một task cụ thể.

**Path Parameters**:
- `id`: ID của task (integer)

**Ví dụ Request**:
```bash
GET /api/tasks/1
```

**Response (200 OK)**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "Task 1",
    "description": "Description here",
    "completed": false,
    "priority": "High",
    "created_at": "2025-11-01T10:00:00",
    "updated_at": "2025-11-01T10:00:00"
  }
}
```

**Response (404 Not Found)**:
```json
{
  "success": false,
  "error": "Task not found"
}
```

---

#### 7.2.3. POST /api/tasks

**Mô tả**: Tạo task mới.

**Request Body**:
```json
{
  "title": "New Task",        // Required
  "description": "Description", // Optional
  "priority": "High"           // Optional: "High", "Medium", "Low"
}
```

**Ví dụ Request**:
```bash
POST /api/tasks
Content-Type: application/json

{
  "title": "Complete project",
  "description": "Finish TaskMaster application",
  "priority": "High"
}
```

**Response (201 Created)**:
```json
{
  "success": true,
  "data": {
    "id": 5,
    "title": "Complete project",
    "description": "Finish TaskMaster application",
    "completed": false,
    "priority": "High",
    "created_at": "2025-11-01T10:00:00",
    "updated_at": "2025-11-01T10:00:00"
  },
  "message": "Task created successfully"
}
```

**Response (400 Bad Request)**:
```json
{
  "success": false,
  "error": "Title is required"
}
```

---

#### 7.2.4. PUT /api/tasks/<id>

**Mô tả**: Cập nhật task.

**Path Parameters**:
- `id`: ID của task

**Request Body** (có thể chỉ gửi các field cần update):
```json
{
  "title": "Updated Title",     // Optional
  "description": "New desc",   // Optional
  "completed": true,            // Optional
  "priority": "Low"            // Optional
}
```

**Ví dụ Request**:
```bash
PUT /api/tasks/1
Content-Type: application/json

{
  "completed": true,
  "priority": "High"
}
```

**Response (200 OK)**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "Updated Title",
    "description": "New desc",
    "completed": true,
    "priority": "High",
    "created_at": "2025-11-01T10:00:00",
    "updated_at": "2025-11-01T11:00:00"
  },
  "message": "Task updated successfully"
}
```

---

#### 7.2.5. DELETE /api/tasks/<id>

**Mô tả**: Xóa task.

**Path Parameters**:
- `id`: ID của task

**Ví dụ Request**:
```bash
DELETE /api/tasks/1
```

**Response (200 OK)**:
```json
{
  "success": true,
  "message": "Task deleted successfully"
}
```

**Response (404 Not Found)**:
```json
{
  "success": false,
  "error": "Task not found"
}
```

---

#### 7.2.6. GET /api/tasks/search?q=<query>

**Mô tả**: Tìm kiếm tasks theo từ khóa.

**Query Parameters**:
- `q` (required): Từ khóa tìm kiếm

**Ví dụ Request**:
```bash
GET /api/tasks/search?q=project
```

**Response (200 OK)**:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "title": "Complete project",
      ...
    }
  ],
  "count": 1,
  "query": "project"
}
```

---

#### 7.2.7. GET /api/tasks/export/csv

**Mô tả**: Export danh sách tasks ra file CSV.

**Ví dụ Request**:
```bash
GET /api/tasks/export/csv
```

**Response (200 OK)**:
- Content-Type: `text/csv`
- Content-Disposition: `attachment; filename=tasks_export_20251101_120000.csv`
- Body: CSV file content

---

#### 7.2.8. GET /api/tasks/export/json

**Mô tả**: Export danh sách tasks ra file JSON.

**Ví dụ Request**:
```bash
GET /api/tasks/export/json
```

**Response (200 OK)**:
- Content-Type: `application/json`
- Content-Disposition: `attachment; filename=tasks_export_20251101_120000.json`
- Body: JSON file content

---

## 8. HƯỚNG DẪN CÀI ĐẶT

### 8.1. Yêu cầu hệ thống

- Docker Desktop (Windows/Mac) hoặc Docker Engine + Docker Compose (Linux)
- Git
- 2GB RAM trở lên
- Port 5001 và 3307 trống

### 8.2. Cài đặt với Docker (Khuyến nghị)

```bash
# 1. Clone repository
git clone https://github.com/munzinh/pythonnangcao.git
cd pythonnangcao

# 2. Khởi động ứng dụng
docker-compose up --build

# 3. Truy cập ứng dụng
# Web: http://localhost:5001
# API: http://localhost:5001/api/tasks
```

### 8.3. Kiểm tra cài đặt

```bash
# Kiểm tra containers đang chạy
docker-compose ps

# Kiểm tra logs
docker-compose logs web
docker-compose logs db

# Kiểm tra database
docker-compose exec db mysql -u todo_user -ptodo_password taskmaster_db -e "SHOW TABLES;"
```

### 8.3.1. Cách Xem MySQL Database Sau Khi Deploy Docker

Sau khi deploy lên Docker, bạn có thể xem database MySQL theo nhiều cách:

#### **Cách 1: Sử dụng MySQL Command Line trong Container (Khuyến nghị)**

```bash
# 1. Truy cập vào MySQL container
docker-compose exec db bash

# 2. Kết nối vào MySQL
mysql -u todo_user -ptodo_password taskmaster_db

# 3. Thực hiện các câu lệnh SQL
mysql> SHOW TABLES;
mysql> SELECT * FROM tasks;
mysql> DESCRIBE tasks;
mysql> EXIT;

# 4. Thoát khỏi container
exit
```

**Hoặc chạy một lần từ host machine:**

```bash
# Xem tất cả tables
docker-compose exec db mysql -u todo_user -ptodo_password taskmaster_db -e "SHOW TABLES;"

# Xem toàn bộ dữ liệu trong bảng tasks
docker-compose exec db mysql -u todo_user -ptodo_password taskmaster_db -e "SELECT * FROM tasks;"

# Xem cấu trúc bảng tasks
docker-compose exec db mysql -u todo_user -ptodo_password taskmaster_db -e "DESCRIBE tasks;"

# Đếm số lượng tasks
docker-compose exec db mysql -u todo_user -ptodo_password taskmaster_db -e "SELECT COUNT(*) FROM tasks;"

# Xem tasks chưa hoàn thành
docker-compose exec db mysql -u todo_user -ptodo_password taskmaster_db -e "SELECT * FROM tasks WHERE completed = 0;"
```

#### **Cách 2: Sử dụng MySQL Workbench hoặc DBeaver**

1. **Tải MySQL Workbench**: https://dev.mysql.com/downloads/workbench/
2. **Tạo kết nối mới** với thông tin:
   - **Host**: `localhost`
   - **Port**: `3307` (quan trọng! Port đã được map trong docker-compose.yml)
   - **Username**: `todo_user`
   - **Password**: `todo_password`
   - **Schema**: `taskmaster_db`

3. **Test Connection** và Connect

#### **Cách 3: Sử dụng phpMyAdmin (Docker Add-on)**

Thêm service phpMyAdmin vào `docker-compose.yml`:

```yaml
services:
  # ... existing services ...
  
  phpmyadmin:
    image: phpmyadmin/phpmyadmin
    container_name: taskmaster_phpmyadmin
    restart: always
    environment:
      PMA_HOST: db
      PMA_PORT: 3306
      PMA_USER: todo_user
      PMA_PASSWORD: todo_password
    ports:
      - "8080:80"
    depends_on:
      - db
```

Sau đó:
```bash
docker-compose up -d phpmyadmin
# Truy cập: http://localhost:8080
```

#### **Cách 4: Sử dụng HeidiSQL (Windows) hoặc Sequel Pro (Mac)**

**HeidiSQL (Windows)**:
- Download: https://www.heidisql.com/download.php
- Tạo kết nối: `localhost:3307`, user: `todo_user`, password: `todo_password`

**Sequel Pro / Sequel Ace (Mac)**:
- Download: https://sequel-ace.com/
- Host: `127.0.0.1`, Port: `3307`, User: `todo_user`, Password: `todo_password`

#### **Cách 5: Sử dụng VS Code Extension**

1. Cài đặt extension **"MySQL"** trong VS Code
2. Tạo connection với:
   - Host: `localhost`
   - Port: `3307`
   - User: `todo_user`
   - Password: `todo_password`
   - Database: `taskmaster_db`

#### **Kiểm tra Container MySQL đang chạy:**

```bash
# Xem trạng thái MySQL container
docker-compose ps db

# Xem logs của MySQL
docker-compose logs db

# Xem logs real-time
docker-compose logs -f db

# Kiểm tra port mapping
docker port taskmaster_mysql
```

#### **Thông tin kết nối Database (Từ file docker-compose.yml):**

| Thuộc tính | Giá trị |
|------------|---------|
| Container Name | `taskmaster_mysql` |
| Host (từ máy host) | `localhost` hoặc `127.0.0.1` |
| Port (từ máy host) | `3307` ⚠️ |
| Port (trong container) | `3306` |
| Database Name | `taskmaster_db` |
| Username | `todo_user` |
| Password | `todo_password` |
| Root Password | `rootpassword` |

⚠️ **Lưu ý quan trọng**: Port được map là `3307:3306`, nghĩa là từ máy host bạn phải dùng port `3307` chứ không phải `3306`!

### 8.4. Troubleshooting

**Lỗi port đã được sử dụng:**
- Sửa ports trong `docker-compose.yml`

**Lỗi kết nối database:**
```bash
docker-compose restart db
docker-compose logs db
```

**Reset hoàn toàn:**
```bash
docker-compose down -v
docker-compose up --build
```

---

## 9. DEMO VÀ THUYẾT TRÌNH

### 9.1. Demo Flow (Thứ tự thuyết trình)

#### Bước 1: Giới thiệu dự án (2 phút)
- Tên dự án: TaskMaster
- Mục đích: Quản lý công việc cá nhân
- Công nghệ sử dụng: Flask, MySQL, Docker, Bootstrap 5

#### Bước 2: Kiến trúc hệ thống (3 phút)
- Giải thích sơ đồ 3 tầng: Frontend → Backend → Database
- Design Patterns: Factory, Blueprint, ORM, Repository
- Cấu trúc thư mục

#### Bước 3: Demo tính năng (5 phút)
- **Tạo task**: Tạo task mới với title, description, priority
- **Xem danh sách**: Hiển thị tất cả tasks
- **Cập nhật**: Edit task, đánh dấu hoàn thành
- **Xóa**: Xóa task với confirmation
- **Tìm kiếm**: Tìm kiếm real-time
- **Export**: Export CSV và JSON

#### Bước 4: Giải thích luồng hoạt động (3 phút)
- Chọn 1 tính năng (ví dụ: tạo task)
- Giải thích luồng từ Frontend → API → TaskManager → Database
- Hiển thị code snippets

#### Bước 5: Database và API (2 phút)
- Database schema
- API endpoints
- Response format

#### Bước 6: Docker và Deployment (2 phút)
- Cách chạy với Docker
- Lợi ích của containerization
- Hướng dẫn deploy

#### Bước 7: Q&A (3 phút)
- Trả lời câu hỏi

### 9.2. Code Snippets quan trọng để trình bày

#### 9.2.1. Application Factory
```python
# app/__init__.py
def create_app(config_name=None):
    app = Flask(__name__)
    config = config_by_name.get(config_name, config_by_name['default'])
    app.config.from_object(config)
    db.init_app(app)
    migrate = Migrate(app, db)
    CORS(app)
    
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app
```

#### 9.2.2. Task Model
```python
# app/models.py
class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    priority = db.Column(db.String(20), default='Medium')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

#### 9.2.3. API Endpoint
```python
# app/api/routes.py
@bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    task = TaskManager.create_task(
        title=data['title'],
        description=data.get('description'),
        priority=data.get('priority', 'Medium')
    )
    return jsonify({'success': True, 'data': task}), 201
```

#### 9.2.4. Business Logic
```python
# app/models.py - TaskManager
@staticmethod
def create_task(title, description=None, priority='Medium'):
    if not title or not title.strip():
        raise ValueError("Task title không được để trống")
    task = Task(title=title.strip(), description=description, priority=priority)
    db.session.add(task)
    db.session.commit()
    return task.to_dict()
```

### 9.3. Các điểm nhấn khi thuyết trình

1. **Kiến trúc rõ ràng**: 
   - Tách biệt Frontend, Backend, Database
   - Sử dụng Design Patterns chuẩn

2. **Code Quality**:
   - Clean code, dễ đọc
   - Có comments giải thích
   - Error handling đầy đủ

3. **RESTful API**:
   - API chuẩn REST
   - Response format nhất quán
   - Proper HTTP status codes

4. **Docker Ready**:
   - Dễ deploy
   - Isolated environment
   - Production-ready

5. **User Experience**:
   - Giao diện đẹp, responsive
   - Real-time search
   - Export data

### 9.4. Câu hỏi thường gặp và câu trả lời

**Q: Tại sao dùng Flask thay vì Django?**
A: Flask nhẹ, linh hoạt, phù hợp với dự án nhỏ. Django phù hợp hơn cho ứng dụng lớn, phức tạp.

**Q: Tại sao dùng SQLAlchemy?**
A: ORM giúp không cần viết SQL thủ công, dễ maintain, hỗ trợ nhiều database engines.

**Q: Tại sao dùng Docker?**
A: Đảm bảo môi trường nhất quán, dễ deploy, isolated, production-ready.

**Q: Có thể mở rộng thêm tính năng gì?**
A: User authentication, categories, due dates, notifications, team collaboration, etc.

**Q: Hiệu năng như thế nào?**
A: Sử dụng indexing cho các trường thường query, connection pooling cho production.

---

## KẾT LUẬN

TaskMaster là một ứng dụng quản lý công việc hoàn chỉnh với:

✅ **Kiến trúc rõ ràng**: 3-tier architecture  
✅ **Code quality**: Clean code, Design Patterns  
✅ **RESTful API**: Chuẩn REST, dễ mở rộng  
✅ **Docker Ready**: Dễ deploy  
✅ **User Experience**: Giao diện đẹp, tính năng đầy đủ  

**Công nghệ**: Flask, MySQL, SQLAlchemy, Docker, Bootstrap 5  
**Patterns**: Factory, Blueprint, ORM, Repository  
**Features**: CRUD, Search, Filter, Export  

---

*Tài liệu này được tạo để hỗ trợ thuyết trình và hiểu rõ luồng hoạt động của ứng dụng TaskMaster.*

