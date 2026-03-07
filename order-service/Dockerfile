# 1. Use official Python image
FROM python:3.12-slim

# 2. Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Set working directory
WORKDIR /app

# 4. Install dependencies
COPY app/requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# 5. Copy project
COPY app/ .

# 6. Collect static files (optional for Nginx serving)
RUN python manage.py collectstatic --noinput

# 7. Run the server (for dev)
CMD ["gunicorn", "order_service.wsgi:application", "--bind", "0.0.0.0:8000"]