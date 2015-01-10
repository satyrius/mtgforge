import os
from .common import *  # NOQA

ALLOWED_HOSTS = ['*']

API_HOST = os.environ.get('API_HOST', 'api.topdeck.pro')

# Absolute filesystem path to the directory that will hold user-uploaded files.
MEDIA_ROOT = '/var/www/mtgforge-media/'
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = 'http://{host}/media/'.format(host=API_HOST)

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
STATIC_ROOT = '/var/www/mtgforge-static/'


ADMINS = (
    ('Anton Egorov', 'anton.egoroff@gmail.com'),
)

MANAGERS = ADMINS
