"""

"""


def upload_path_exe(instance, filename):
    """
    Create a directory to store the algorithm binary and other data.

    :param instance:
    :param filename:
    :return:
    """
    return 'app_{id}/{filename}'.format(id=instance.id.hex, filename=filename)