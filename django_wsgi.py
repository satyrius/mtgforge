import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.prod'

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
