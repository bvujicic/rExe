import logging
import os
import shutil
import zipfile

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.text import slugify


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
    return 'app_{app_name}/{filename}'.format(app_name=slugify(instance.name, allow_unicode=False), filename=filename)


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
    filename = '{media_root}/{output_directory}/archive/results.zip'.format(
        media_root=settings.MEDIA_ROOT,
        output_directory=iteration.output_directory
    )
    try:
        with zipfile.ZipFile(file=filename, mode='w') as archive:
            for root, dir, files in os.walk(iteration.output_directory):
                if root == os.path.dirname(filename):
                    continue

                for file in files:
                    archive.write(filename=os.path.join(root, file))

    except Exception as exc:
        logger.exception(exc)


def add_user_access(*, user):
    """
    Scans all algorithms and creates access for this user to those that have set auto_add flag.

    :param user: (User)
    :return:
    """
    from web.models import Algorithm

    for algorithm in Algorithm.objects.all():
        if algorithm.auto_add:
            # add this user to user list
            algorithm.users.add(user)


def send_activation_mail(*, request, user):
    """
    Generate activation token and construct activation URL.

    :param user: (User) Registered user instance.
    """
    token = default_token_generator.make_token(user=user)
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

    requested_host = request.META['HTTP_HOST']

    path = reverse_lazy('register_confirm', kwargs={'uidb64': uidb64, 'token': token})

    url = '{schema}://{domain}{path}'.format(schema=schema, domain=domain, path=path)

    template = loader.get_template('email/registration.html')
    message = template.render(context=Context({'url': url}))

    # send activation mail
    user.email_user(
        subject=_('rExe portal - aktivacija korisničkog računa'),
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL
    )


def verify_activation_token(*, uidb64, token):
    """
    :param uidb64: (str) Base 64 of user PK.
    :param token: (str) Hash.
    :return: (bool) True if user verified, False otherwise.
    """
    user_id = force_text(urlsafe_base64_decode(uidb64))

    try:
        user = User.objects.get(pk=user_id)

    except User.DoesNotExist:
        return False

    else:
        # activate user if token is alright
        if default_token_generator.check_token(user=user, token=token):
            if not user.is_active:
                user.is_active = True
                user.save()

            return True

        else:
            return False