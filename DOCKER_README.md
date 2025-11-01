# Hướng dẫn Docker cho TaskMaster

## Yêu cầu
- Docker Desktop (Windows/Mac) hoặc Docker Engine + Docker Compose (Linux)
- Git (nếu chưa có)

## Cách sử dụng

### 1. Khởi động ứng dụng với Docker Compose

```bash
# Build và start tất cả services (MySQL + Flask)
docker-compose up --build

# Hoặc chạy ở background
docker-compose up -d --build
```

### 2. Truy cập ứng dụng

- **Web Interface**: http://localhost:5001 (port 5000 có thể bị chiếm bởi ứng dụng khác)
- **MySQL Database**: localhost:3307 (port 3306 có thể bị chiếm bởi MySQL local)
  - Username: `todo_user`
  - Password: `todo_password`
  - Database: `taskmaster_db`

### 3. Các lệnh thường dùng

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

# Chạy migrations thủ công
docker-compose exec web flask db upgrade
```

### 4. Thay đổi cấu hình

Nếu muốn thay đổi password, database name, v.v.:
1. Sửa file `docker-compose.yml`
2. Sửa biến môi trường trong `docker-compose.yml` (section `environment` của service `web`)
3. Rebuild: `docker-compose up --build`

### 5. Database Migration

Migrations sẽ chạy tự động khi container khởi động. Nếu cần chạy thủ công:

```bash
docker-compose exec web flask db upgrade
```

### 6. Backup Database

```bash
# Export database
docker-compose exec db mysqldump -u todo_user -ptodo_password taskmaster_db > backup.sql

# Import database
docker-compose exec -T db mysql -u todo_user -ptodo_password taskmaster_db < backup.sql
```

## Cấu trúc Docker

- **Dockerfile**: Định nghĩa image cho Flask app
- **docker-compose.yml**: Định nghĩa services (MySQL + Flask)
- **init.sql**: Script khởi tạo database khi MySQL container start lần đầu
- **.dockerignore**: Loại trừ các file không cần thiết khi build image

## Troubleshooting

### Lỗi kết nối database
- Kiểm tra MySQL container đã chạy: `docker-compose ps`
- Kiểm tra logs: `docker-compose logs db`

### Lỗi port đã được sử dụng
- Ports đã được cấu hình: Web = 5001, MySQL = 3307
- Nếu cần đổi, sửa trong `docker-compose.yml` (ví dụ: `"5002:5000"` cho web, `"3308:3306"` cho MySQL)

### Reset hoàn toàn
```bash
docker-compose down -v
docker-compose up --build
```

