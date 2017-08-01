import os
import zipfile

from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from django.dispatch import receiver

from ipware.ip import get_ip

from web.tasks import execute_algorithm
from web.models import Iteration, LoginHistory


@receiver(user_logged_in)
def save_login_ip_address(sender, request, user, **kwargs):
    """
    Save IP address of the user that logged in.
    """
    try:
        ip_address = get_ip(request=request)
        LoginHistory.objects.create(user=user, address=ip_address)

    except Exception:
        pass


@receiver(post_save, sender=Iteration)
def extract_iteration_archive(sender, instance, created, **kwargs):
    """
    Extract zipped input file.
    """
    if not created:
        return

    try:
        with zipfile.ZipFile(file=instance.input_data.file) as archive:
            archive.extractall(path=os.path.dirname(instance.input_data.path))

    except zipfile.BadZipfile as exc:
        pass


@receiver(post_save, sender=Iteration)
def create_iteration_job(sender, instance, created, **kwargs):
    """
    Delegates execution of algorithm to Celery worker.
    """
    if not created:
        return

    result = execute_algorithm.apply_async(task_id=instance.id, kwargs={'algorithm_path': instance.algorithm.file.path})

    return result