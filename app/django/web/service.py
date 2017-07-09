"""

"""


def upload_path_exe(instance, filename):
    """
    Create a directory to store the algorithm binary and other data.

    :param instance:
    :param filename:
    :return:
    """
    return 'app_{app_id}/{filename}'.format(app_id=instance.id.hex, filename=filename)


def upload_path_input_data(instance, filename):
    from web.models import Iteration

    iteration_count = Iteration.objects.filter(user=instance.user).count() + 1

    return 'app_{app_id}/{user_id}/{iteration_count}/in/{filename}'.format(
        app_id=instance.algorithm.id.hex,
        user_id=instance.user.id,
        iteration_count=iteration_count,
        filename=filename
    )