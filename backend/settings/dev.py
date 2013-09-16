import os
from settings.common import *

DEBUG = True
TEMPLATE_DEBUG = True
MEDIA_DEV_MODE = True
DEBUG_SERP = True

# Django's normal exception handling of view functions will be suppressed,
# and exceptions will propagate upwards.
DEBUG_PROPAGATE_EXCEPTIONS = True

# Controls what the behavior is when an unhandled exception occurs.
TASTYPIE_FULL_DEBUG = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
STATIC_ROOT = '/tmp/mtgforge/static/'

# Use filebased cache backend for development to make setup easier for
# developers. Do not force them to install memcache server.
CACHES['default'] = {
    'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
    'LOCATION': '/tmp/mtgforge/cache/',
}

# Log database requests to the comsole output
if os.getenv('DEBUG_DB'):
    LOGGING['loggers']['django.db'] = {
        'handlers': ['console'],
        'level': 'DEBUG',
        'propagate': True,
    }

# Log all oracle management commangs messages
LOGGING['loggers']['oracle.management']['level'] = 'DEBUG'

# Enable django debug toolbar
#MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + (
#    'debug_toolbar.middleware.DebugToolbarMiddleware',
#)

from settings.local import *
