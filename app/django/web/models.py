import uuid

from django.conf import settings
from django.utils.functional import cached_property
from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from django_utils.abstract import TimestampModel

from web.service import upload_path_exe, upload_path_input_data


class Algorithm(TimestampModel):
    """
    Information and binaries connected to an algorithm/application for remote execution.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(verbose_name='naziv', max_length=255, unique=True)
    file = models.FileField(verbose_name='datoteka za izvršavanje', upload_to=upload_path_exe)
    description = models.TextField(verbose_name='opis', blank=True)
    document = models.FileField(verbose_name='datoteka dokumentacije', blank=True, upload_to=upload_path_exe)
    source = models.FileField(verbose_name='datoteka source kȏda', blank=True, upload_to=upload_path_exe)
    is_active = models.BooleanField(
        verbose_name='aktivno',
        default=True,
        help_text='Neaktivan algoritam se neće prikazivati kao opcija korisnicima.'
    )
    auto_add = models.BooleanField(
        verbose_name='automatski pristup korisnicima',
        default=True,
        help_text='Omogućiti kako bi se novi registrirani korisnici automatski dodali u listu korisnika s pristupom.'
    )
    users = models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='korisnici s pristupom', blank=True)

    class Meta:
        verbose_name = 'algoritam'
        verbose_name_plural = 'algoritmi'
        db_table = 'algorithm'
        ordering = ('-created',)

    def __str__(self):
        return self.name


class Iteration(TimestampModel):
    """
    A single iteration of algorith execution and all connected input/output data.
    """
    START = 1
    FAILURE = -1
    SUCCESS = 0
    STATUS_CHOICES = (
        (START, _('izvršavanje u tijeku')),
        (FAILURE, _('neuspješno završeno')),
        (SUCCESS, _('uspješno završeno')),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    input_data = models.FileField(verbose_name='ulazni podaci', upload_to=upload_path_input_data, max_length=511)
    output_data = models.FileField(verbose_name='izlazni podaci', blank=True, max_length=511)
    status_code = models.SmallIntegerField(
        verbose_name='statusni kod',
        choices=STATUS_CHOICES,
        null=True,
        blank=True,
        default=START
    )
    status_message = models.TextField(verbose_name='statusna poruka', blank=True)
    mail_on_completion = models.BooleanField(verbose_name='pošalji rezultate na mail', default=False)
    mailed = models.DateTimeField(verbose_name='poslano', null=True)
    finished = models.DateTimeField(verbose_name='završetak', null=True)

    algorithm = models.ForeignKey(to='web.Algorithm', verbose_name='algoritam', on_delete=models.PROTECT)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='korisnik', on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'iteracija algoritma'
        verbose_name_plural = 'iteracije algoritma'
        db_table = 'algorithm_iteration'
        ordering = ('-created', 'algorithm')

    def __str__(self):
        return str(self.id)

    @staticmethod
    def _is_image(file_data):
        from PIL import Image

        try:
            image = Image.open(self.input_data)

        except (OSError, ValueError) as exc:
            # not an image
            return False

        else:
            image.verify()
            return True

    @property
    def input_is_image(self):
        return  self._is_image(file_data=self.input_data)

    @property
    def output_is_image(self):
        return self._is_image(file_data=self.input_data)

    @property
    def started(self):
        return self.status_code == self.START

    @property
    def failed(self):
        return self.status_code == self.FAILURE

    @property
    def successful(self):
        return self.status_code == self.SUCCESS

    @cached_property
    def iteration_number(self):
        manager = self.__class__.objects

        if self.created is None:
            number = manager.filter(algorithm=self.algorithm, user=self.user, created__lte=now()).count() + 1
        else:
            number = manager.filter(algorithm=self.algorithm, user=self.user, created__lte=self.created).count()

        return number

    @property
    def input_directory(self):
        return self._data_directory('in')

    @property
    def output_directory(self):
        return self._data_directory('out')

    def _data_directory(self, location):
        return 'app_{app_name}/{user_id}/{iteration_number}/{location}'.format(
            app_name=slugify(self.algorithm.name, allow_unicode=False),
            user_id=self.user_id,
            iteration_number=self.iteration_number,
            location=location
        )


class LoginHistory(TimestampModel):
    """
    Simple login IP recording model.
    """
    address = models.GenericIPAddressField(verbose_name='IP adresa prijave', protocol='both')
    data = models.TextField(verbose_name='dodatni podaci')

    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='korisnik')

    class Meta:
        verbose_name = 'unos povijesti logiranja'
        verbose_name_plural = 'unosi povijesti logiranja'
        db_table = 'login_history'
        ordering = ('-created',)

    def __str__(self):
        return self.address

