import zipfile

from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from django.dispatch import receiver

from ipware.ip import get_ip

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
def extract_archive(sender, instance, **kwargs):
    """
    Extract zipped input file.
    """
    try:
        with zipfile.ZipFile(file=instance.input_data.file) as archive:
            archive.extractall()

    except zipfile.BadZipfile as exc:
        print(exc)
        pass