import zipfile

from django.db.models.signals import post_save
from django.dispatch import receiver

from web.models import Iteration


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