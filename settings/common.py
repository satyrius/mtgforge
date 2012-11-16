# -*- coding: utf-8 -*-
import os
import sys

# Django settings for mtgforge project.

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DIR_NAME = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'mtgforge',                      # Or path to database file if using sqlite3.
        'USER': 'postgres',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        'OPTIONS': {
            'autocommit': True,
        }
    }
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

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(DIR_NAME, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '/tmp/mtg-static/'

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
    os.path.join(DIR_NAME, 'static'),
]

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# experiment with mediagenerator (alternative asset manager and compression tool)
MEDIA_DEV_MODE = 'runserver' in sys.argv  # do not compress media under ./manage.py runserver
PRODUCTION_MEDIA_URL = '/static/gm/'
GENERATED_MEDIA_DIR = os.path.join(DIR_NAME, '_generated_media/gm')
GLOBAL_MEDIA_DIRS = STATICFILES_DIRS[:] # force mediagenerator to do not walk over _generated_media dir
DEV_MEDIA_URL = '/static-dev/'
ROOT_MEDIA_FILTERS = {}
MEDIA_BLOCKS = False

STATICFILES_DIRS.append(os.path.join(DIR_NAME, '_generated_media'))


# Make this unique, and don't share it with anybody.
SECRET_KEY = '32fcsn31khb%-3m$iu1hs@i_l$)woq88m*_*$-k31z-9z3m!c^'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'mediagenerator.middleware.MediaMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)
INTERNAL_IPS = ('127.0.0.1',)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(DIR_NAME, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    # Third-party apps
    'debug_toolbar',
    'django_extensions',
    'mediagenerator',
    'modeltranslation',
    'oracle',
    'tastypie',

    # Our apps
    'forge',
    'south',

    'django_nose', # it should be after south (http://pypi.python.org/pypi/django-nose, Caveats)
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/tmp/django_cache',
    },
    'provider_page': {
        'BACKEND': 'oracle.providers.cache.PageCache',
    },
}

# Use Django Nose test runner.
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = ['--verbosity=2', '--with-id']

# South’s test runner integration will make the test database be created using
# syncdb, rather than via migrations.
SOUTH_TESTS_MIGRATE = True

# Modeltranslation settings.
# http://code.google.com/p/django-modeltranslation/wiki/InstallationAndUsage03
gettext = lambda s: s
LANGUAGES = (
    ('en', gettext('English')),
    ('ru', gettext('Русский')),
    ('tw', gettext('繁體中文')),
    ('cn', gettext('简体中文')),
    ('de', gettext('Deutsch')),
    ('fr', gettext('Français')),
    ('it', gettext('Italiano')),
    ('jp', gettext('日本語')),
    ('ko', gettext('한국어')),
    ('pt', gettext('Português')),
    ('es', gettext('Español')),
)
MODELTRANSLATION_DEFAULT_LANGUAGE = 'en'
MODELTRANSLATION_TRANSLATION_REGISTRY = 'translation'

# Data provider settings
DATA_PROVIDER_TIMEOUT = 10 # Ten seconds
DATA_PROVIDER_CACHE_TIMEOUT = 60 * 60 * 2 # Two hours

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}
