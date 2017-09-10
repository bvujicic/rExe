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
    name = models.CharField(verbose_name=_('naziv'), max_length=255, unique=True)
    file = models.FileField(verbose_name=_('datoteka za izvršavanje'), upload_to=upload_path_exe)
    description = models.TextField(verbose_name=_('opis'), blank=True)
    document = models.FileField(verbose_name=_('datoteka dokumentacije'), blank=True, upload_to=upload_path_exe)
    source = models.FileField(verbose_name=_('datoteka source kȏda'), blank=True, upload_to=upload_path_exe)
    is_active = models.BooleanField(
        verbose_name=_('aktivno'),
        default=True,
        help_text=_('Neaktivan algoritam se neće prikazivati kao opcija korisnicima.')
    )
    auto_add = models.BooleanField(
        verbose_name=_('automatski pristup korisnicima'),
        default=True,
        help_text=_('Omogućiti kako bi se novi registrirani korisnici automatski dodali u listu korisnika s pristupom.')
    )
    users = models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name=_('korisnici s pristupom'), blank=True)

    class Meta:
        verbose_name = _('algoritam')
        verbose_name_plural = _('algoritmi')
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
    input_data = models.FileField(verbose_name=_('ulazni podaci'), upload_to=upload_path_input_data, max_length=511)
    output_data = models.FileField(verbose_name=_('izlazni podaci'), blank=True, max_length=511)
    status_code = models.SmallIntegerField(
        verbose_name=_('statusni kod'),
        choices=STATUS_CHOICES,
        null=True,
        blank=True,
        default=START
    )
    status_message = models.TextField(verbose_name=_('statusna poruka'), blank=True)
    mail_on_completion = models.BooleanField(verbose_name=_('pošalji rezultate na mail'), default=False)
    mailed = models.DateTimeField(verbose_name=_('poslano'), null=True)
    finished = models.DateTimeField(verbose_name=_('završetak'), null=True)

    algorithm = models.ForeignKey(to='web.Algorithm', verbose_name=_('algoritam'), on_delete=models.PROTECT)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name=_('korisnik'), on_delete=models.PROTECT)

    class Meta:
        verbose_name = _('iteracija algoritma')
        verbose_name_plural = _('iteracije algoritma')
        db_table = 'algorithm_iteration'
        ordering = ('-created', 'algorithm')

    def __str__(self):
        return str(self.id)

    @property
    def input_is_image(self):
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
    def output_is_image(self):
        from PIL import Image

        try:
            image = Image.open(self.output_data)

        except (OSError, ValueError):
            # not an image
            return False

        else:
            image.verify()
            return True


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
    address = models.GenericIPAddressField(verbose_name=_('adresa logiranja'), protocol='both')
    data = models.TextField(verbose_name=_('dodatni podaci'))

    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name=_('korisnik'))

    class Meta:
        verbose_name = _('unos povijesti logiranja')
        verbose_name_plural = _('unosi povijesti logiranja')
        db_table = 'login_history'
        ordering = ('-created',)

    def __str__(self):
        return self.address

