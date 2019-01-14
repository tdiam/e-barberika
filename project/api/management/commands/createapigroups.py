from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = 'Creates the designated user groups for the API'

    def handle(self, *args, **options):
        Group.objects.get_or_create(name='Volunteer')
