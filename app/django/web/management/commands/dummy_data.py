from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from web.models import Algorithm


class Command(BaseCommand):

    def handle(self, *args, **options):
        User = get_user_model()

        User.objects.create_superuser(username='admin', email='', password='1')