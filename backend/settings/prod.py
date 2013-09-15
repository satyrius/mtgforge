from settings.common import *

# Absolute filesystem path to the directory that will hold user-uploaded files.
MEDIA_ROOT = '/var/www/mtgforge-media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
STATIC_ROOT = '/var/www/mtgforge-static/'

ADMINS = (
    ('Anton Egorov', 'anton.egoroff@gmail.com'),
)

MANAGERS = ADMINS

from settings.local import *
