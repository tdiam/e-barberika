import json

from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model

from ..models import Token
from ..views import TokenAuthRegisterView

User = get_user_model()

class TokenAuthRegisterViewTestCase(TestCase):
    '''Checks the functionality of the TokenAuthRegisterView'''

    def setUp(self):
        # Create user
        self.username = 'johndoe'
        self.password = 'johndoe'
        self.email = 'johndoe@asoures.gr'
        self.user = User.objects.create_user(self.username, password=self.password, email=self.email)

        # Request factory
        self.factory = RequestFactory()

        # View
        self.view = TokenAuthRegisterView.as_view()

    def test_cant_create_user_with_same_username(self):
        request = self.factory.post('/',{
            'username': self.username,
            'password': 'whatever',
            'email': 'anything@da.gr'
        })

        response = self.view(request)
        self.assertEqual(response.status_code, 400)

    def test_cant_create_user_with_same_email(self):
        request = self.factory.post('/', {
            'username': 'matt murdock',
            'password': 'whatever',
            'email': self.email
        })

        response = self.view(request)
        self.assertEqual(response.status_code, 400)

    def test_can_register_user(self):
        User.objects.filter(username='mattmurdock').delete()

        request = self.factory.post('/',{
            'username': 'mattmurdock',
            'password': 'definitely blind',
            'email': 'matt@nelsonandmurdock.com'
        })

        response = self.view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.filter(username='mattmurdock').exists(), True)
