# -*- coding: utf-8 -*-
import os
import dj_database_url
from os.path import join, dirname, abspath
from contrib import l10n

DEBUG = False
TEMPLATE_DEBUG = False

PROJECT_ROOT = abspath(join(dirname(__file__), '../../..'))
APP_ROOT = os.environ.get(
    'DJANGO_APP_ROOT', os.path.join(PROJECT_ROOT, 'backend'))

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': dj_database_url.config(default='postgres://localhost/mtgforge')
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = [
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'backend', 'oracle', 'static'),
]

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

DEFAULT_FILE_STORAGE = 'storages.backends.hashpath.HashPathStorage'


# Make this unique, and don't share it with anybody.
SECRET_KEY = '32fcsn31khb%-3m$iu1hs@i_l$)woq88m*_*$-k31z-9z3m!c^'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)
INTERNAL_IPS = ('127.0.0.1',)

ROOT_URLCONF = 'topdeck.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'topdeck.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'client', 'public'),
    os.path.join(APP_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'grappelli',
    'grappelli_modeltranslation',
    'django.contrib.admin',

    'debug_toolbar',
    'django_extensions',
    'modeltranslation',
    'storages',
    'tastypie',

    # Our apps
    'crawler',
    'forge',
    'oracle',

    'south',
    'django_nose',  # it should be after south (http://pypi.python.org/pypi/django-nose, Caveats)
)

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': 'localhost:11211',
        'OPTIONS': {
            'MAX_ENTRIES': 100000
        }
    },
}

# Modeltranslation settings.
# http://code.google.com/p/django-modeltranslation/wiki/InstallationAndUsage03
gettext = lambda s: s
LANGUAGES = (
    (l10n.EN, gettext('English')),
    (l10n.RU, gettext('Русский')),
    (l10n.TW, gettext('繁體中文')),
    (l10n.CN, gettext('简体中文')),
    (l10n.DE, gettext('Deutsch')),
    (l10n.FR, gettext('Français')),
    (l10n.IT, gettext('Italiano')),
    (l10n.JP, gettext('日本語')),
    (l10n.KO, gettext('한국어')),
    (l10n.PT, gettext('Português')),
    (l10n.ES, gettext('Español')),
)
MODELTRANSLATION_DEFAULT_LANGUAGE = l10n.EN
MODELTRANSLATION_TRANSLATION_FILES = (
    'oracle.translation',
)


def gen_null_string(max_length):
    from model_mommy import generators
    return generators.gen_string(max_length)
gen_null_string.required = ['max_length']

MOMMY_CUSTOM_FIELDS_GEN = {
    'contrib.fields.NullCharField': gen_null_string,
}

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'oracle.management': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}

# Log database requests to the console output
if os.getenv('DEBUG_DB'):
    LOGGING['loggers']['django.db'] = {
        'handlers': ['console'],
        'level': 'DEBUG',
        'propagate': True,
    }

GRAPPELLI_ADMIN_TITLE = 'MTG Forge'

CARD_IMAGE_SERP_THUMB = '223x310'
CARD_IMAGE_THUMBS = [CARD_IMAGE_SERP_THUMB]

# Only JSON, baby!
TASTYPIE_DEFAULT_FORMATS = ['json']

# This will add additional information to the SERP resource
DEBUG_SERP = False
