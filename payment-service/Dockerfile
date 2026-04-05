# 1. Use official Python image
FROM python:3.12-slim

# 2. Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=payment_service.settings 
ENV SECRET_KEY=dummy
ENV DEBUG=1

# 3. Set working directory
WORKDIR /app

# 4. Install dependencies
COPY app/requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# 5. Copy project
COPY app/ .

# 6. Expose port
EXPOSE 8000

# 7. Entry point: run collectstatic & migrations, then start server
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn payment_service.wsgi:application --bind 0.0.0.0:8000 & python start_consumer.py"]