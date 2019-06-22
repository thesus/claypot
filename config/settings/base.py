"""
Django settings for claypot project.

Generated by 'django-admin startproject' using Django 2.1.1.
"""
from datetime import timedelta

import environ


ROOT_DIR = environ.Path(__file__) - 3
APPS_DIR = ROOT_DIR.path("claypot")

env = environ.Env()
env.read_env(str(ROOT_DIR.path(env.path("ENVIRONMENT_FILE", ".env"))))

DEBUG = env.bool("DJANGO_DEBUG", default=False)

SECRET_KEY = env("DJANGO_SECRET_KEY")

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=[])

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.humanize",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    "rest_framework",
    "django_filters",
    "django_rq",
]

INSTALLED_APPS += ["claypot", "claypot.api", "claypot.images"]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

if DEBUG:
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
    INTERNAL_IPS = ["::1", "127.0.0.1"]
    TEMPLATES[0]["DIRS"] += ["claypot/contrib"]

WSGI_APPLICATION = "config.wsgi.application"


# Database

DATABASES = {"default": env.db("DATABASE_URL")}


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation."
        "UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation." "MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation." "CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation." "NumericPasswordValidator"},
]


# Internationalization

LANGUAGE_CODE = env("LANGUAGE_CODE", default="en-us")

TIME_ZONE = env("TIME_ZONE", default="UTC")

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files and Media (CSS, JavaScript, Images)

STATIC_ROOT = str(ROOT_DIR("static"))
STATIC_URL = "/static/"

MEDIA_ROOT = env("MEDIA_ROOT", default=str(APPS_DIR("media")))
MEDIA_URL = "/media/"

IMAGE_ROOT = env("IMAGE_ROOT", default=str(ROOT_DIR("images")))

# Image sizes for resizing and thumbnail
# If both dimensions are given, the image will be cropped. (center)
IMAGE_SIZES = {"small": {"w": 500}, "medium": {"w": 900}, "large": {"w": 1400}}

THUMBNAIL_SIZE = {"w": 400, "h": 400}

# Email
EMAIL_CONFIG = env.email_url("EMAIL_URL", default="consolemail://")
vars().update(EMAIL_CONFIG)

# Rest Framework
REST_FRAMEWORK = {
    "AUTHENTICATION_BACKENDS": ("rest_framework.authentication.SessionAuthentication"),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 30,
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ),
}


# Disable browsable html renderer in production and setup SSL_HEADER for proxy
if not DEBUG:
    REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = "rest_framework.renderers.JSONRenderer"
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# Django RQ
RQ_QUEUES = {
    "default": {"HOST": env("REDIS_HOST", default="localhost"), "PORT": 6379, "DB": 0}
}

# Configures (production) error logging for both Django and django-rq, if set.
SENTRY_DSN = env("SENTRY_DSN", default="")

# Sentry logging for frontend.
# Defaults to same key as backend since it also uses the new DSN format (without the private key).
SENTRY_FRONTEND_DSN = env("SENTRY_FRONTEND_DSN", default=SENTRY_DSN)

if SENTRY_DSN:
    from sentry_sdk import init
    from sentry_sdk.integrations.django import DjangoIntegration

    init(dsn=SENTRY_DSN, integrations=[DjangoIntegration()])

RECIPE_DELETE_GRACE_PERIOD = timedelta(
    seconds=env.int("RECIPE_DELETE_GRACE_PERIOD", default=3600)
)
