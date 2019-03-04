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

        # update react .env with api base url
        with open('project/client/.env', 'w') as dotenv:
            dotenv.write(f'\nREACT_APP_API_URL="https://asoures.gr:{PORT}/observatory/api/"\n')

        # re-build frontend, to use the correct REACT_APP_API_URL
        # os.system(f'cd project/client && echo "Building ReactJS" && npm run build > /dev/null')

        # create directory for static files
        print('Collecting static files')
        os.system('python manage.py collectstatic --noinput')

        # start server
        os.system(f'mod_wsgi-express start-server --log-to-terminal --startup-log --https-port {PORT} --https-only --server-name asoures.gr --ssl-certificate-file ssl/server.crt --ssl-certificate-key-file ssl/server.key --url-alias /static static --application-type module project.wsgi')
