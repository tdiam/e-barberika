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
        #   `X-TOKEN-AUTH: Token xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
        # i.e. the keyword `Token` followed by the token UUID
        auth_header = request.META.get(app_settings.TOKEN_AUTH_HEADER, '').split()

        # If user passed no token header or an invalid token header, ignore
        if not auth_header or auth_header[0].lower() != 'token':
            return self.get_response(request, *args, **kwargs)

        # If token header is valid, get token and try to authenticate
        user = authenticate(token=auth_header[1])
        if user:
            # If successful, store user instance in request
            request.user = user

        # Continue to next middleware
        return self.get_response(request, *args, **kwargs)
