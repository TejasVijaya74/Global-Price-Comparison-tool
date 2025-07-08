
"""
Celery worker for background tasks
"""
from celery import Celery
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Celery
celery_app = Celery(
    'price_comparison_worker',
    broker=os.getenv('REDIS_URL', 'redis://localhost:6379/0'),
    backend=os.getenv('REDIS_URL', 'redis://localhost:6379/0'),
    include=['tasks']
)

# Configure Celery
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_routes={
        'tasks.scrape_vendor': {'queue': 'scraping'},
        'tasks.update_prices': {'queue': 'pricing'},
    }
)

if __name__ == '__main__':
    celery_app.start()
