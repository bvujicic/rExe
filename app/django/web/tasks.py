import subprocess
import sys
import time

import django
from django.conf import settings
from django.utils.timezone import now
from celery import shared_task, Task, states
from celery.exceptions import Ignore

from app.celery import celery_logger
from web.service import create_archive



class send_mail():
    pass


class IterationTask(Task):

    @staticmethod
    def _iteration(task_id):
        django.setup()
        from web.models import Iteration

        return Iteration.objects.get(id=task_id)

    def _update_iteration(self, task_id, status_code, exception=None):
        """
        :param task_id: Iteration ID to retrieve
        :param code: Status code of Iteration
        """
        iteration = self._iteration(task_id)

        iteration.status_code = status_code
        iteration.status_message = exception if exception is not None else ''
        iteration.finished = now()

        iteration.save(update_fields=['status_code', 'status_message', 'finished'])

    def on_success(self, retval, task_id, args, kwargs):
        """
        Mark task as succesful.
        """
        django.setup()
        from web.models import Iteration

        print('success')
        self._update_iteration(task_id=task_id, status_code=Iteration.SUCCESS)
        create_archive(iteration=self._iteration(task_id))

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
    """
    Task that spawns another child process that will execute the algorithm.

    :param self: Task istance
    :param algorithm_path: Path of the executable.

    :return:
    """
    process = subprocess.run(
        algorithm_path,
        check=True,
        timeout=settings.SUBPROCESS_TIMEOUT
    )
