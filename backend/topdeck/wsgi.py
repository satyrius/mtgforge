import os
import sys
from os.path import dirname

# Force prod settings for WSGI server
# os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.prod'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'topdeck.settings.prod')

# Fix python path
sys.path.append(dirname(__file__))

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
