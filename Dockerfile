# Sử dụng Python 3.11 slim image để tối ưu kích thước
# Nếu gặp lỗi timeout, có thể thử: python:3.10-slim hoặc python:3.9-slim
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Cài đặt các dependencies hệ thống (cần cho PyMySQL)
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements và cài đặt Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ ứng dụng
COPY . .

# Expose port 5000
EXPOSE 5000

# Set biến môi trường mặc định
ENV FLASK_APP=run.py
ENV FLASK_ENV=production
ENV FLASK_HOST=0.0.0.0
ENV FLASK_PORT=5000

# Chạy migrations và start server
CMD ["sh", "-c", "flask db upgrade && python run.py"]

