#1. Môi trường Python 3.11 bản nhẹ
FROM python:3.11-slim

#2. Thư mục làm việc bên trong máy ảo 
WORKDIR /app

#3. Coppy danh sách thư viện
COPY requirements.txt .

#4. Cài đặt thư viện trong requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

