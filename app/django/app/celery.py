import os

from celery import Celery
from celery.utils.log import get_task_logger


celery_logger = get_task_logger(__name__)

celery_app = Celery(main='app', broker='redis://localhost:6379/0')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

celery_app.conf.update(
    task_track_started=True
    #result_backend='db+postgresql://devel:devel@localhost/rexe'
)
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()
