FROM python:3.11-slim

WORKDIR /app

# Copy file thu vien vao truoc
COPY requirements.txt .

# Cai dat thu vien (dung psycopg2-binary se rat nhanh)
RUN pip install --no-cache-dir -r requirements.txt

# Copy toan bo code
COPY . .

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "src.back_end.main:app", "--host", "0.0.0.0", "--port", "8000"]