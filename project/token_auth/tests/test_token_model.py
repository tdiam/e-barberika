from datetime import timedelta

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils.timezone import now

from ..models import Token
from .. import settings as app_settings


User = get_user_model()

class TokenModelTestCase(TestCase):
    '''Test suite for the Token model used in our API'''

    def setUp(self):
        '''Create a user and a token for them'''
        self.user = User.objects.create_user('gooduser', 'good@user.com', 'gooduser')
        self.token = Token(user=self.user)
        self.token.save()

    def test_token_expiration_works(self):
        '''Change creation timestamp so that the token would have expired'''
        self.token.created_at = now() - timedelta(**app_settings.TOKEN_EXPIRATION) - timedelta(seconds=1)
        self.token.save()

        self.assertFalse(Token.objects.filter(key=self.token.key).exists())
