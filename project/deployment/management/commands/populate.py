import os
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Starts the https server at PORT'
    requires_migrations_checks = True
    requires_system_checks = True

    def add_arguments(self, parser):
        pass
        # parser.add_argument('port', default=8443, type=int)

    def handle(self, *args, **options):
        # for some reason could not import from settings
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(
            os.path.dirname(os.path.dirname(__file__))
        )))

        print('Not yet implemented (:')

        # add shops and products
