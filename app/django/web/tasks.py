import time

from celery import shared_task

from app.celery import celery_logger


@shared_task(track_started=True, bind=True)
def execute_algorithm(self):
    print(self.request)
    time.sleep(15)

    celery_logger.info('hello')
