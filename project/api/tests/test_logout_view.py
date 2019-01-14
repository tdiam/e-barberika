from django.conf import settings
from django.test import TestCase
from django.contrib.auth import get_user_model

from project.token_auth.models import Token
from .helpers import ApiRequestFactory
from ..middleware import ParseUrlEncodedParametersMiddleware as ApiMiddleware
from ..views import LogoutView


User = get_user_model()

class TokenAuthLogoutViewTestCase(TestCase):
    '''Checks the functionality of the LogoutView'''

    def setUp(self):
        # Create user
        self.username = 'johndoe'
        self.password = 'johndoe'
        self.user = User.objects.create_user(self.username, password=self.password)

        self.factory = ApiRequestFactory()
        self.view = ApiMiddleware(LogoutView.as_view())
        self.url = settings.API_ROOT

    def test_logout_removes_tokens(self):
        '''Checks that logging out removes all tokens associated with that user'''
        # Create a token for the user
        token = Token(user=self.user)
        token.save()

        request = self.factory.post(self.url)
        request.user = self.user
        response = self.view(request)

        self.assertEqual(response.status_code, 200)
        # Check that the created token no longer exists
        self.assertEqual(Token.objects.filter(user=self.user).count(), 0)

    def test_logout_when_not_logged_in(self):
        '''Logout should return 204 when no user is logged in'''
        # request.user will not be set
        request = self.factory.post(self.url)
        response = self.view(request)

        self.assertEqual(response.status_code, 204)
