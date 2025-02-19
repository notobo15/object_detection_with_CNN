# Sử dụng Python 3.8 vì TensorFlow 2.4.1 hỗ trợ tốt phiên bản này
FROM python:3.8

# Thiết lập biến môi trường tránh tạo bytecode Python
ENV PYTHONUNBUFFERED=1

# Cài đặt thư viện hệ thống cần thiết cho OpenCV & TensorFlow
RUN apt-get update && apt-get install -y \
    libsm6 libxext6 libxrender-dev libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Đặt thư mục làm việc trong container
WORKDIR /app

# Sao chép file requirements.txt vào container
COPY setup.txt .

# Cài đặt các thư viện Python
RUN pip install --no-cache-dir -r setup.txt

# Sao chép toàn bộ mã nguồn vào container
COPY . .

# Migrate database
RUN python manage.py migrate

# Thu thập static files (nếu có)
RUN python manage.py collectstatic --noinput

# Mở cổng 8000 để chạy server Django
EXPOSE 8000

# Chạy ứng dụng Django bằng Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "server.wsgi:application"]
