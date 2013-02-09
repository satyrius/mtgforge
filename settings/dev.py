import os
from common import *


DEBUG = True
TEMPLATE_DEBUG = True
MEDIA_DEV_MODE = True

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
MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)
