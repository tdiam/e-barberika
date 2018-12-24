'''App-specific settings that can be overridden by the global settings file'''
from django.conf import settings

# First look at TOKEN_AUTH_URL_PREFIX setting
# If not set, try API_ROOT
TOKEN_AUTH_URL_PREFIX = getattr(settings, 'TOKEN_AUTH_URL_PREFIX', '/')
if not TOKEN_AUTH_URL_PREFIX:
    TOKEN_AUTH_URL_PREFIX = getattr(settings, 'API_ROOT', '/')

TOKEN_AUTH_HEADER = getattr(settings, 'TOKEN_AUTH_HEADER', 'HTTP_X_TOKEN_AUTH')

TOKEN_EXPIRATION = getattr(settings, 'TOKEN_EXPIRATION', {'hours': 1})
