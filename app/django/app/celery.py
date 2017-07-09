from celery import Celery
import time


celery = Celery(main='app', broker='redis://localhost:6379/0')

celery.conf.update(
    task_track_started=True,
    #result_backend='db+postgresql://devel:devel@localhost/rexe'
)


@celery.task(track_started=True)
def execute_algorithm():
    time.sleep(15)

    return 'hello'
