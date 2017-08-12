import logging
import os
import shutil
import zipfile


logger = logging.getLogger('web')


def _app_folder(instance):
    return 'app_{app_id}'.format(app_id=instance.id.hex)


def _archive_folder(iteration, location, filename):
    from web.models import Iteration

    iteration_count = Iteration.objects.filter(user=iteration.user).count() + 1

    return '{app_folder}/{user_id}/{iteration_count}/{location}/archive/{filename}'.format(
        app_folder=_app_folder(iteration.algorithm),
        user_id=iteration.user.id,
        iteration_count=iteration_count,
        location=location,
        filename=filename
    )

def upload_path_exe(instance, filename):
    """
    Create a directory to store the algorithm binary and other data.

    :param instance:
    :param filename:
    :return:
    """
    return '{app_folder}/{filename}'.format(app_folder=_app_folder(instance), filename=filename)


def upload_path_input_data(instance, filename):
    return _archive_folder(iteration=instance, location='in', filename=filename)


def extract_archive(*, file_name):
    """
    Extracts archive to specified location. If it's a bad archive file ignore silently and log the error.

    :param file_name: (str) Path to which directory to extract.
    :return:
    """
    try:
        with zipfile.ZipFile(file=file_name) as archive:
            archive.extractall(path=os.path.join(os.path.dirname(file_name), os.pardir))

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
    folder_path = os.path.abspath(_archive_folder(iteration=iteration, location='out', filename='results.zip'))
    #os.mkdir(os.path.dirname(folder_path))
    try:
        with zipfile.ZipFile(file=folder_path, mode='w') as archive:
            for root, dir, files in os.walk(folder_path):
                for file in files:
                    archive.write(os.path.join(root, file))

    except Exception as exc:
        logger.exception(exc)
