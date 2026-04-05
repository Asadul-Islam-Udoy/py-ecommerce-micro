import os
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "order_service.settings")
django.setup()

from app.consumer import start_consumer

if __name__ == "__main__":
    start_consumer()