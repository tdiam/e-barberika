import json

from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model

from ..models import Token
from ..views import ObtainTokenLoginView


User = get_user_model()

class ObtainTokenViewTestCase(TestCase):
    '''Checks the functionality of the ObtainTokenLoginView'''

    def setUp(self):
        # Create user
        self.username = 'johndoe'
        self.password = 'johndoe'
        self.user = User.objects.create_user(self.username, password=self.password)

        self.factory = RequestFactory()
        self.view = ObtainTokenLoginView.as_view()

    def test_can_obtain_token(self):
        '''User can login, parse token and token is same as in database'''

        request = self.factory.post('/', {
            'username': self.username,
            'password': self.password
        })

        response = self.view(request)
        self.assertEqual(response.status_code, 200)

        try:
            parsed = json.loads(response.content)
        except json.JSONDecodeError:
            self.fail('JSON could not be parsed from response')

        token = parsed['token']
        check = Token.objects.get(key=token)

        self.assertEqual(check.user.username, self.username)

    def test_fail_for_invalid_user(self):
        '''Checks that view returns 401-Unauthorized if fake credentials are given'''

        request = self.factory.post('/', {
            'username': 'fakeuser',
            'password': 'fakeuser'
        })

        response = self.view(request)
        self.assertEqual(response.status_code, 401)

    def test_keep_same_token(self):
        '''Checks that token remains the same after two consecutive logins.

        NOTE: This may fail if TOKEN_EXPIRATION is too small, since the token
        may expire between the two requests.
        '''

        request = self.factory.post('/', {
            'username': self.username,
            'password': self.password
        })

        response = self.view(request)
        first_token = json.loads(response.content)['token']

        response = self.view(request)
        second_token = json.loads(response.content)['token']

        self.assertEqual(first_token, second_token)
