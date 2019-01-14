from django.test import TestCase, RequestFactory
from django.views import View
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from ..middleware import TokenAuthMiddleware
from ..models import Token
from .. import settings as app_settings


User = get_user_model()

def test_view(_req):
    '''A test view'''
    return HttpResponse('OK')

class TokenAuthMiddlewareTestCase(TestCase):
    '''Test suite for the TokenAuthMiddleware used in our API'''

    def setUp(self):
        # Create user
        self.user = User.objects.create_user('johndoe', password='johndoe')

        # Create token for user
        self.token = Token(user=self.user)
        self.token.save()

        # Format token header
        self.token_header = str(self.token.key)

        # Request factory
        self.factory = RequestFactory()

        # Initialize middleware
        self.middleware = TokenAuthMiddleware(test_view)

    def test_can_access_with_token(self):
        '''Checks if middleware authenticates user with valid token'''

        # The following trick is employed because the header name
        # is variable (app_settings.TOKEN_AUTH_HEADER) and must
        # be passed as a keyword argument.
        request = self.factory.get(app_settings.TOKEN_AUTH_URL_PREFIX, **{
            app_settings.TOKEN_AUTH_HEADER: self.token_header
        })
        # Send request with no user logged in
        request.user = AnonymousUser()

        # Middleware should change request.user to self.user since their token was given
        _response = self.middleware(request)

        # Check if user was logged in successfully
        self.assertEqual(request.user.username, self.user.username)

    def test_cant_access_without_token(self):
        '''Checks if middleware does not authenticate when no token is provided'''
        # Pass no token in headers
        request = self.factory.get(app_settings.TOKEN_AUTH_URL_PREFIX)
        request.user = AnonymousUser()

        _response = self.middleware(request)

        # Check if no user was authenticated
        self.assertTrue(request.user.is_anonymous)

    def test_cant_access_with_invalid_token(self):
        '''Checks if middleware does not authenticate when invalid token is provided'''
        request = self.factory.get(app_settings.TOKEN_AUTH_URL_PREFIX, **{
            app_settings.TOKEN_AUTH_HEADER: 'not-a-valid-uuid-token'
        })
        request.user = AnonymousUser()

        _response = self.middleware(request)

        # Check if no user was authenticated
        self.assertTrue(request.user.is_anonymous)

    def test_cant_access_with_fake_token(self):
        '''Checks if middleware does not authenticate when fake token is provided'''
        faketoken = Token.fake.get()

        request = self.factory.get(app_settings.TOKEN_AUTH_URL_PREFIX, **{
            app_settings.TOKEN_AUTH_HEADER: str(faketoken)
        })
        request.user = AnonymousUser()

        _response = self.middleware(request)

        # Check if no user was authenticated
        self.assertTrue(request.user.is_anonymous)
