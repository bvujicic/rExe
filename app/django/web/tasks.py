import subprocess
import sys
import time


import django
from celery import shared_task, Task, states
from celery.exceptions import Ignore

from app.celery import celery_logger



class IterationTask(Task):

    @staticmethod
    def _update_iteration(task_id, status_code, exception=None):
        """
        :param task_id: Iteration ID to retrieve
        :param code: Status code of Iteration
        """
        django.setup()
        from web.models import Iteration

        iteration = Iteration.objects.get(id=task_id)

        iteration.status_code = status_code
        iteration.status_message = exception if exception is not None else ''

        iteration.save(update_fields=['status_code', 'status_message'])

    def on_success(self, retval, task_id, args, kwargs):
        """
        Mark task as succesful.
        """
        django.setup()
        from web.models import Iteration

        print('success')
        self._update_iteration(task_id=task_id, status_code=Iteration.SUCCESS)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """
        Mark task as failure.
        """
        django.setup()
        from web.models import Iteration

        print('fail')
        self._update_iteration(task_id=task_id, status_code=Iteration.FAILURE, exception=einfo)


@shared_task(base=IterationTask, track_started=True, bind=True, acks_late=True)
def execute_algorithm(self, algorithm_path):

    process = subprocess.run(f'python {algorithm_path}', check=True, timeout=60, shell=True)
