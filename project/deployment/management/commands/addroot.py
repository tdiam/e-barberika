from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Starts the http server at PORT'
    requires_migrations_checks = True
    requires_system_checks = True

    def add_arguments(self, parser):
        parser.add_argument('name', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('pass', type=str)

    def handle(self, *args, **options):
        # for some reason could not import from settings
        get_user_model().objects.create_superuser(
            options['name'], options['email'], options['pass']
        )
