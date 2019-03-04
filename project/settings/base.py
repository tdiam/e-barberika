'''Sets default configuration parameters and imports from environment'''
import dj_database_url
from corsheaders.defaults import default_headers as cors_default_headers

from .env import env_bool, env_list, env_setting, abs_path, env_str


DEBUG = env_bool('DEBUG', False)
ALLOWED_HOSTS = env_list('ALLOWED_HOSTS', ['*'] if DEBUG else [])
SECRET_KEY = env_str('SECRET_KEY', 'secret' if DEBUG else '')


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'corsheaders',
    'project.token_auth',
    'project.api',
    'project.deployment'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'project.token_auth.middleware.TokenAuthMiddleware',
    'project.api.middleware.ObservatoryContentTypeMiddleware',
    'project.api.middleware.ParseUrlEncodedParametersMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'project.token_auth.backends.TokenAuthBackend',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

ROOT_URLCONF = 'project.urls'
WSGI_APPLICATION = 'project.wsgi.application'
DATABASES = {'default': dj_database_url.config()}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

STATIC_URL = env_str('STATIC_URL', '/static/')
STATIC_ROOT = env_str('STATIC_ROOT', abs_path('static'))


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Athens'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Available levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': env_setting('LOG_LEVEL', 'INFO'),
            'class': 'logging.StreamHandler',
        }
    },
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': env_setting('LOG_LEVEL', 'INFO'),
            'propagate': True
        }
    }
}

# CORS settings
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_HEADERS = cors_default_headers + (
    'X-OBSERVATORY-AUTH',
)

# API root path
API_ROOT = '/observatory/api/'

# Token Auth settings

# X-OBSERVATORY-AUTH header is translated to
# HTTP_X_OBSERVATORY_AUTH in Django's request handlers
TOKEN_AUTH_HEADER = 'HTTP_X_OBSERVATORY_AUTH'

TOKEN_EXPIRATION = {
    'hours': 4,
}

# Needed for react
REACT_APP = abs_path('project/client/build/')
STATICFILES_DIRS = (
    REACT_APP,
    abs_path(REACT_APP + 'static/'),
)

REACT_APP_INDEX_HTML = abs_path(REACT_APP + 'index.html')
