from django.test import TestCase
from django.contrib.auth import get_user_model, authenticate

from ..models import Token


User = get_user_model()

class TokenAuthBackendTestCase(TestCase):
    '''Test suite for the TokenAuthBackend used in our API'''

    def setUp(self):
        self.user = User.objects.create_user('johndoe', password='johndoe')
        self.token = Token(user=self.user)
        self.token.save()

    def test_realtoken_can_login(self):
        '''Checks if user can be authenticated by their token'''
        check = authenticate(token=self.token.key)
        self.assertEqual(self.user.username, check.username)

    def test_faketoken_cant_login(self):
        '''Checks if authentication with fake token fails'''

        faketoken = Token.fake.get()

        check = authenticate(token=faketoken)
        self.assertIsNone(check)
