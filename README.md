# MySQL Setup Guide

## Hướng dẫn chuyển đổi từ SQLite sang MySQL

### Bước 1: Cài đặt MySQL Server

#### Windows:
1. Tải MySQL Installer từ: https://dev.mysql.com/downloads/installer/
2. Chạy installer và chọn "Developer Default"
3. Thiết lập root password
4. Khởi động MySQL Service

#### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install mysql-server
sudo mysql_secure_installation
```

#### macOS:
```bash
brew install mysql
brew services start mysql
mysql_secure_installation
```

### Bước 2: Tạo Database và User

Kết nối MySQL với quyền root:
```sql
mysql -u root -p
```

Tạo database và user:
```sql
-- Tạo database
CREATE DATABASE todo_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE test_todo_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Tạo user
CREATE USER 'todo_user'@'localhost' IDENTIFIED BY 'password';

-- Cấp quyền
GRANT ALL PRIVILEGES ON todo_db.* TO 'todo_user'@'localhost';
GRANT ALL PRIVILEGES ON test_todo_db.* TO 'todo_user'@'localhost';

-- Áp dụng thay đổi
FLUSH PRIVILEGES;

-- Thoát
EXIT;
```

### Bước 3: Cài đặt Dependencies

```bash
pip install -r requirements.txt
```

### Bước 4: Cấu hình Environment

1. Copy file mẫu:
```bash
cp env.example .env
```

2. Chỉnh sửa file `.env`:
```env
DATABASE_URI=mysql+pymysql://todo_user:password@localhost/todo_db
TEST_DATABASE_URI=mysql+pymysql://todo_user:password@localhost/test_todo_db
SECRET_KEY=your-secret-key-change-in-production
FLASK_ENV=development
```

**Lưu ý:** Thay `password` bằng password thực tế bạn đã tạo cho user `todo_user`.

### Bước 5: Khởi chạy Application

```bash
python backend/app.py
python frontend/gui.py
```

Lần đầu chạy sẽ tự động tạo bảng `tasks` trong MySQL.


### Bước 7: Kiểm tra

1. **Kiểm tra API:**
```bash
curl http://localhost:5000/health
```

2. **Kiểm tra database:**
```sql
mysql -u todo_user -p todo_db
SELECT COUNT(*) FROM tasks;
```

### Troubleshooting

#### Lỗi kết nối MySQL:
- Kiểm tra MySQL service đang chạy
- Kiểm tra username/password trong `.env`
- Kiểm tra database đã được tạo

#### Lỗi PyMySQL:
```bash
pip install PyMySQL==1.1.0
```

#### Lỗi encoding:
Đảm bảo database được tạo với charset `utf8mb4`:
```sql
CREATE DATABASE todo_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Cấu trúc Database

Bảng `tasks` sẽ có cấu trúc:
- `id`: INT PRIMARY KEY AUTO_INCREMENT
- `title`: VARCHAR(200) NOT NULL
- `description`: TEXT
- `completed`: BOOLEAN DEFAULT FALSE
- `priority`: VARCHAR(20) DEFAULT 'Medium'
- `created_at`: DATETIME NOT NULL
- `updated_at`: DATETIME NOT NULL

### Performance Notes

- Đã thêm indexes cho các trường thường xuyên query: `title`, `completed`, `priority`, `created_at`
- Sử dụng connection pooling với `pool_pre_ping=True`

### Backup & Restore

#### Backup:
```bash
mysqldump -u todo_user -p todo_db > backup.sql
```

#### Restore:
```bash
mysql -u todo_user -p todo_db < backup.sql
```
