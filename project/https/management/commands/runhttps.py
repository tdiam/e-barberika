import os
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Starts the https server at PORT'
    requires_migrations_checks = True
    requires_system_checks = True

    def add_arguments(self, parser):
        parser.add_argument('port', default=8443, type=int)

    def handle(self, *args, **options):
        # for some reason could not import from settings
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(
            os.path.dirname(os.path.dirname(__file__))
        )))
        PORT = options['port']

        # switch to BASE_DIR
        os.chdir(BASE_DIR)

        # create directory for static files
        os.system('python manage.py collectstatic --noinput')

        # start server
        os.system(f'mod_wsgi-express start-server --log-to-terminal --startup-log --https-port {PORT} --https-only --server-name asoures.gr --ssl-certificate-file ssl/server.crt --ssl-certificate-key-file ssl/server.key --url-alias /static static --application-type module project.wsgi')
