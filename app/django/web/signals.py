import logging
import os
import zipfile

from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from ipware.ip import get_ip

from web.tasks import execute_algorithm
from web.models import Iteration, LoginHistory
from web.service import extract_archive, create_archive, _prepare_directories


logger = logging.getLogger('web')


@receiver(user_logged_in)
def save_login_ip_address(sender, request, user, **kwargs):
    """
    Save IP address of the user that logged in.
    """
    try:
        ip_address = get_ip(request=request)
        http_user_agent = request.META.get('HTTP_USER_AGENT', '')

        LoginHistory.objects.create(user=user, address=ip_address, data=http_user_agent)

    except Exception as exc:
        logger.exception(exc)


@receiver(pre_save, sender=Iteration)
def prepare_directories(sender, instance, **kwargs):
    """
    Prepare directory structure for the iteration.
    """
    if instance._state.adding:
        _prepare_directories(iteration=instance)


@receiver(post_save, sender=Iteration)
def extract_iteration_input_data(sender, instance, created, **kwargs):
    """
    Extract archived input file.
    """
    if created:
        try:
            with zipfile.ZipFile(file=instance.input_data.file) as archive:
                # just check if ZIP file is valid
                archive.testzip()

        except zipfile.BadZipFile as exc:
            logger.info('Not a ZIP file. Skipping extraction.')

        else:
            extract_archive(iteration=instance)


@receiver(pre_save, sender=Iteration)
def archive_iteration_output_data(sender, instance, **kwargs):
    """
    Create archive from output data.
    """
    if instance._state.adding:
        return

    create_archive(iteration=instance)


@receiver(post_save, sender=Iteration)
def create_iteration_job(sender, instance, created, **kwargs):
    """
    Delegates execution of algorithm to Celery worker.
    """
    if not created:
        return

    result = execute_algorithm.apply_async(task_id=instance.id, kwargs={'algorithm_path': instance.algorithm.file.path})

    return result