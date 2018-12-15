from django.test import TestCase, RequestFactory
from django.views import View
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied

from ..middleware import TokenAuthMiddleware
from ..models import Token
from .. import settings as app_settings


User = get_user_model()

class TestView(LoginRequiredMixin, View):
    '''Test view that requires authorization.

    For class-based views the `LoginRequiredMixin` is used:
    https://docs.djangoproject.com/el/2.1/topics/auth/default/#the-loginrequired-mixin
    '''

    # Will raise 403 if authorization fails
    raise_exception = True

    def get(self, request):
        return HttpResponse('Hello.')

class TokenAuthMiddlewareTestCase(TestCase):
    '''Test suite for the TokenAuthMiddleware used in our API'''

    def setUp(self):
        # Create user
        self.user = User.objects.create_user('johndoe', password='johndoe')

        # Create token for user
        self.token = Token(user=self.user)
        self.token.save()

        # Format token header
        self.token_header = f'Token {self.token.key}'

        # Request factory
        self.factory = RequestFactory()

        # Initialize middleware
        self.middleware = TokenAuthMiddleware(TestView.as_view())

    def test_can_access_with_token(self):
        '''Checks if protected view can be accessed by user's token'''

        # The following trick is employed because the header name
        # is variable (app_settings.TOKEN_AUTH_HEADER) and must
        # be passed as a keyword argument.
        request = self.factory.get(app_settings.TOKEN_AUTH_URL_PREFIX, **{
            app_settings.TOKEN_AUTH_HEADER: self.token_header
        })
        # Send request with no user logged in
        request.user = AnonymousUser()

        # Middleware should change request.user to self.user since their token was given
        response = self.middleware(request)

        # Check if request succeeded
        self.assertEqual(response.status_code, 200)
        # Check if user was logged in successfully
        self.assertEqual(request.user.username, self.user.username)

    def test_cant_access_without_token(self):
        '''Checks if protected view cannot be accessed without a valid token'''
        faketoken = Token.fake.get()

        request = self.factory.get(app_settings.TOKEN_AUTH_URL_PREFIX, **{
            app_settings.TOKEN_AUTH_HEADER: str(faketoken)
        })
        # Send request with no user logged in
        request.user = AnonymousUser()

        # Authentication should fail and the view should raise 403
        with self.assertRaises(PermissionDenied):
            _response = self.middleware(request)
