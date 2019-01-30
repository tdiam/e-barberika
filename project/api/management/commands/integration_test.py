import os
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Runs integration tests'

    def handle(self, *args, **options):
        # for some reason could not import from settings
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(
            os.path.dirname(os.path.dirname(__file__))
        )))

        # switch to BASE_DIR
        os.chdir(BASE_DIR)

        # run tests
        os.system('python manage.py test project.api.tests.integration.IntegrationTests.IntegrationTests')
