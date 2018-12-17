from datetime import timedelta
import uuid

from django.db import models
from django.conf import settings
from django.utils.timezone import now

from . import settings as app_settings


class TokenExpirationManager(models.Manager):
    def get_queryset(self):
        '''Deletes expired tokens and then returns original queryset'''

        # From this time and beyond, all tokens are valid
        threshold = now() - timedelta(**app_settings.TOKEN_EXPIRATION)
        # Delete tokens before this time
        super().get_queryset().filter(created_at__lt=threshold).delete()

        return super().get_queryset()

class FakeTokenManager(models.Manager):
    '''Provides a method get() that returns a non-existent token.

    Example:
    ```
        fake = Token.fake.get()
    ```
    '''
    def get(self):
        while True:
            faketoken = uuid.uuid4()
            try:
                super().get_queryset().get(key=faketoken)
                continue
            except self.model.DoesNotExist:
                return faketoken

class Token(models.Model):
    '''Token for user authentication in the API.

    `key` is generated automatically as a random UUID identifier.
    Each token is associated with a user.
    Tokens should expire after some time defined in settings.
    '''

    key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.key)

    objects = TokenExpirationManager()
    fake = FakeTokenManager()
