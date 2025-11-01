-- File khởi tạo database cho Docker MySQL
-- File này sẽ được chạy tự động khi container MySQL khởi động lần đầu

-- Đảm bảo database tồn tại
CREATE DATABASE IF NOT EXISTS taskmaster_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Đảm bảo user có quyền truy cập
GRANT ALL PRIVILEGES ON taskmaster_db.* TO 'todo_user'@'%';
FLUSH PRIVILEGES;

