import logging
import os
import shutil
import zipfile

from django.conf import settings


logger = logging.getLogger('web')


def _prepare_directories(iteration):
    os.makedirs('{media_root}/{input_directory}/archive'.format(
        media_root=settings.MEDIA_ROOT,
        input_directory=iteration.input_directory
    ), exist_ok=True)
    os.makedirs('{media_root}/{output_directory}/archive'.format(
        media_root=settings.MEDIA_ROOT,
        output_directory=iteration.output_directory
    ), exist_ok=True)


def upload_path_exe(instance, filename):
    """
    Create a directory to store the algorithm binary and other data.

    :param instance:
    :param filename:
    :return:
    """
    return '{app_name}/{filename}'.format(app_name=instance.name, filename=filename)


def upload_path_input_data(instance, filename):
    return '{input_directory}/archive/{filename}'.format(input_directory=instance.input_directory, filename=filename)


def extract_archive(*, iteration):
    """
    Extracts archive to specified location. If it's a bad archive file ignore silently and log the error.

    :param file_name: (str) Path to which directory to extract.
    :return:
    """
    file_name = iteration.input_data.path
    try:
        with zipfile.ZipFile(file=file_name) as archive:
            archive.extractall(path=os.path.join(settings.MEDIA_ROOT, iteration.input_directory))

    except zipfile.BadZipFile as exc:
        logger.error('Bad ZIP file.')
        logger.exception(exc)

    except Exception as exc:
        logger.error('General error.')
        logger.exception(exc)


def create_archive(*, iteration):
    """
    Creates an archive from the specified folder path.

    :param folder_path:
    :return:
    """
    filename = '{output_directory}/archive/results.zip'.format(output_directory=iteration.output_directory)
    try:
        with zipfile.ZipFile(file=filename, mode='w') as archive:
            for root, dir, files in os.walk(iteration.output_directory):
                if root == os.path.dirname(filename):
                    continue

                for file in files:
                    archive.write(filename=os.path.join(root, file))

    except Exception as exc:
        logger.exception(exc)
