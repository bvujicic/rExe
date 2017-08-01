import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_utils.abstract import TimestampModel

from web.service import upload_path_exe, upload_path_input_data


class Algorithm(TimestampModel):
    """
    Information and binaries connected to an algorithm/application for remote execution.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(verbose_name=_('naziv'), max_length=255)
    file = models.FileField(verbose_name=_('datoteka za izvršenje'), upload_to=upload_path_exe)
    description = models.TextField(verbose_name=_('opis'), blank=True)
    document = models.FileField(verbose_name=_('dokumentacija'), blank=True, upload_to=upload_path_exe)

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
    FAILURE = 2
    SUCCESS = 3
    STATUS_CHOICES = (
        (START, _('pokrenuto')),
        (FAILURE, _('neuspješno završeno')),
        (SUCCESS, _('uspješno završeno')),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    input_data = models.FileField(verbose_name=_('ulazni podaci'), upload_to=upload_path_input_data)
    output_data = models.FileField(verbose_name=_('izlazni podaci'), blank=True)
    status_code = models.SmallIntegerField(
        verbose_name=_('statusni kod'),
        choices=STATUS_CHOICES,
        null=True,
        blank=True,
        default=START
    )
    status_message = models.TextField(verbose_name=_('statusna poruka'), blank=True)

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
    def is_started(self):
        return self.status_code == self.START

    @property
    def is_failed(self):
        return self.status_code == self.FAILURE

    @property
    def is_successful(self):
        return self.status_code == self.SUCCESS


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

