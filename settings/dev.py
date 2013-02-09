import sys
from optparse import OptionParser
from django.core.management.base import BaseCommand
from common import *

parser = OptionParser(prog='dev_settings', option_list=BaseCommand.option_list)
options, args = parser.parse_args(sys.argv[2:])

DEBUG = True
TEMPLATE_DEBUG = True
MEDIA_DEV_MODE = True

# Log database requests to the comsole output
if int(options.verbosity) >= 2:
    LOGGING['loggers']['django.db'] = {
        'handlers': ['console'],
        'level': 'DEBUG',
        'propagate': True,
    }

# Log all oracle management commangs messages
LOGGING['loggers']['oracle.management']['level'] = 'DEBUG'

# Enable django debug toolbar
MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)
