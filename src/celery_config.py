from celery import Celery
import os
from config import REDIS_HOST, REDIS_PORT

celery_app = Celery(
    "notifications",
    broker=f"redis://{REDIS_HOST}:{REDIS_PORT}",
    backend=f"redis://{REDIS_HOST}:{REDIS_PORT}",
)

celery_app.conf.task_routes = {
    'tasks.send_notification': {'queue': 'notifications'}
}
