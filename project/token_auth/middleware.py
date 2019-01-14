from django.contrib.auth import authenticate

from . import settings as app_settings


class TokenAuthMiddleware:
    '''Parses tokens from HTTP header and authenticates user via the token backend.

    Class-based middleware template adapted from:
    https://docs.djangoproject.com/en/2.1/topics/http/middleware/
    '''

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        # Handle only when in API
        if app_settings.TOKEN_AUTH_URL_PREFIX and not request.path.startswith(app_settings.TOKEN_AUTH_URL_PREFIX):
            return self.get_response(request, *args, **kwargs)

        # The auth header must have the following form:
        #   `X-TOKEN-AUTH: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
        token = request.META.get(app_settings.TOKEN_AUTH_HEADER, '')

        # If user passed no token header
        if not token:
            return self.get_response(request, *args, **kwargs)

        # Otherwise, try to authenticate
        user = authenticate(token=token)
        if user:
            # If successful, store user instance in request
            request.user = user

        # Continue to next middleware
        return self.get_response(request, *args, **kwargs)
