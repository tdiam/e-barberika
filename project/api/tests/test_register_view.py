from django.conf import settings
from django.test import TestCase
from django.contrib.auth import get_user_model

from .helpers import ApiRequestFactory
from ..middleware import ParseUrlEncodedParametersMiddleware as ApiMiddleware
from ..views import RegisterView


User = get_user_model()

class TokenAuthRegisterViewTestCase(TestCase):
    '''Checks the functionality of the RegisterView'''

    def setUp(self):
        # Create user
        self.username = 'johndoe'
        self.password = 'johndoe'
        User.objects.create_user(self.username, password=self.password)

        self.factory = ApiRequestFactory()
        self.view = ApiMiddleware(RegisterView.as_view())
        self.url = settings.API_ROOT

    def test_missing_fields_should_fail(self):
        '''Registration without username or password should fail'''
        # Register without password
        request = self.factory.post(self.url, {
            'username': 'mattmurdock'
        })

        response = self.view(request)
        self.assertEqual(response.status_code, 400)

        # Register without username
        request = self.factory.post(self.url, {
            'password': 'definitely blind'
        })

        response = self.view(request)
        self.assertEqual(response.status_code, 400)

    def test_cant_create_user_with_same_username(self):
        '''Registration with existing username should fail'''
        request = self.factory.post(self.url, {
            'username': self.username,
            'password': 'whatever'
        })

        response = self.view(request)
        self.assertEqual(response.status_code, 400)

    def test_can_register_user_and_add_to_volunteers(self):
        '''Registration with new username should succeed and add them to volunteers'''
        request = self.factory.post(self.url, {
            'username': 'mattmurdock',
            'password': 'definitely blind'
        })

        response = self.view(request)

        self.assertEqual(response.status_code, 201)

        user = User.objects.filter(username='mattmurdock')
        self.assertTrue(user.exists())
        user = user.get()
        self.assertTrue(user.groups.filter(name='Volunteer').exists())
