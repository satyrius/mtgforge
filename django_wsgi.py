import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.prod'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
