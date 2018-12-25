import json

from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model

from ..models import Token
from ..views import TokenAuthLogoutView

User = get_user_model()

class LogoutViewTestCase(TestCase):
    '''Checks the functionality of the TokenAuthLogoutView'''

    def setUp(self):
        # Create user
        self.username = 'johndoe'
        self.password = 'johndoe'
        self.user = User.objects.create_user(self.username, password=self.password)

        # Request factory
        self.factory = RequestFactory()

        # View
        self.view = TokenAuthLogoutView.as_view()

    def test_logout_removes_tokens(self):
        '''
        Checks that logging out removes all tokens associated with that user
        '''
        token = Token(user=self.user)
        token.save()

        self.assertNotEqual(Token.objects.filter(user=self.user).count(), 0)

        request = self.factory.post('/')
        request.user = self.user
        response = self.view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Token.objects.filter(user=self.user).count(), 0)

    # REVIEW: other tests?
