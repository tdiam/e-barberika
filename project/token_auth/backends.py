from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .models import Token


# Get currently active user model
# Project may use user model other than the default django.contrib.auth.models.User
# https://docs.djangoproject.com/el/2.1/topics/auth/customizing/#referencing-the-user-model
User = get_user_model()

class TokenAuthBackend:
    '''Enables authentication via tokens.

    Template from:
    https://docs.djangoproject.com/el/2.1/topics/auth/customizing/#writing-an-authentication-backend
    '''

    def authenticate(self, request, token=None):
        '''Receives credentials and must return a user instance or None.'''
        try:
            t = Token.objects.get(key=token)
            return t.user
        except (Token.DoesNotExist, ValidationError):
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
