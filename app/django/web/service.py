"""

"""

def _app_folder(instance):
    return 'app_{app_id}'.format(app_id=instance.id.hex)


def upload_path_exe(instance, filename):
    """
    Create a directory to store the algorithm binary and other data.

    :param instance:
    :param filename:
    :return:
    """
    return '{app_folder}/{filename}'.format(app_folder=_app_folder(instance), filename=filename)


def upload_path_input_data(instance, filename):
    from web.models import Iteration

    iteration_count = Iteration.objects.filter(user=instance.user).count() + 1

    return '{app_folder}/{user_id}/{iteration_count}/in/{filename}'.format(
        app_folder=_app_folder(instance.algorithm),
        user_id=instance.user.id,
        iteration_count=iteration_count,
        filename=filename
    )