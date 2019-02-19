"""
Django settings for claypot project.

Generated by 'django-admin startproject' using Django 2.1.1.
"""

import environ

ROOT_DIR = environ.Path(__file__) - 3
APPS_DIR = ROOT_DIR.path('claypot')

env = environ.Env()
env.read_env(str(ROOT_DIR.path(env.path('ENVIRONMENT_FILE', '.env'))))

DEBUG = env.bool('DJANGO_DEBUG', default=False)

SECRET_KEY = env('DJANGO_SECRET_KEY')

ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=[])

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',

    'rest_framework',
    'django_filters',
]

INSTALLED_APPS += [
    'claypot',
    'claypot.api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

if DEBUG:
    TEMPLATES[0]['DIRS'] += ['claypot/contrib']


WSGI_APPLICATION = 'config.wsgi.application'


# Database

DATABASES = {
    'default': env.db('DATABASE_URL'),
}


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'NumericPasswordValidator',
    },
]


# Internationalization

LANGUAGE_CODE = env('LANGUAGE_CODE', default='en-us')

TIME_ZONE = env('TIME_ZONE', default='UTC')

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files and Media (CSS, JavaScript, Images)

STATIC_ROOT = str(ROOT_DIR('static'))
STATIC_URL = '/static/'

MEDIA_ROOT = str(APPS_DIR('media'))
MEDIA_URL = '/media/'


# Email
EMAIL_BACKEND = env(
    'DJANGO_EMAIL_BACKEND',
    default='django.core.mail.backends.console.EmailBackend'
)

# Rest Framework
REST_FRAMEWORK = {
    'AUTHENTICATION_BACKENDS': (
        'rest_framework.authentication.SessionAuthentication'
    )
}

SENTRY_DSN = env('SENTRY_DSN', default='')
if SENTRY_DSN:
    import raven
    from claypot import __version__
    RAVEN_CONFIG = {
        'dsn': SENTRY_DSN,
        'release': __version__,
    }
    from urllib.parse import urlparse
    _parts = urlparse(SENTRY_DSN)
    _sentry_host = f'{_parts.hostname}'
    if _parts.port is not None:
        _sentry_host += f':{_parts.port}'
    SENTRY_PUBLIC_DSN = env(
        'SENTRY_PUBLIC_DSN',
        default=(
            f'{_parts.scheme}://{_parts.username}@{_sentry_host}{_parts.path}'),
    )
    INSTALLED_APPS += (
        'raven.contrib.django.raven_compat',
    )
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'root': {
            'level': 'WARNING',
            'handlers': ['console', 'sentry'],
        },
        'formatters': {
            'verbose': {
                'format': '%(levelname)s  %(asctime)s  %(module)s '
                          '%(process)d  %(thread)d  %(message)s'
            },
        },
        'handlers': {
            'sentry': {
                'level': 'ERROR', # To capture more than ERROR, change to WARNING, INFO, etc.
                'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
                'tags': {},
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            }
        },
        'loggers': {
            '': {
                'level': 'ERROR',
                'handlers': ['console', 'sentry'],
                'propagate': False,
            },
            'django.db.backends': {
                'level': 'ERROR',
                'handlers': ['console'],
                'propagate': False,
            },
            'raven': {
                'level': 'DEBUG',
                'handlers': ['console'],
                'propagate': False,
            },
            'sentry.errors': {
                'level': 'DEBUG',
                'handlers': ['console'],
                'propagate': False,
            },
        },
    }
