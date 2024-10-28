from celery import Celery
import os
from redis import REDIS_URL

celery_app = Celery(
    "notifications",
    broker=REDIS_URL,
    backend=REDIS_URL,
)

celery_app.conf.task_routes = {
    'tasks.send_notification': {'queue': 'notifications'}
}
