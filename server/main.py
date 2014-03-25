import os
import logging

import django.core.handlers.wsgi
import google.appengine.api.app_logging

# specify the name of your settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

# logging format - waiting here for something better to be available
# (logging at django level would itself be logged as errors by GAE)
for handler in logging.getLogger().handlers:
    if not isinstance(handler, google.appengine.api.app_logging.AppLogsHandler):
        logging.getLogger().debug('setting format for handler %s' % handler)
        formatter = logging.Formatter('%(levelname)s %(asctime)s %(name)s - %(message)s', datefmt='%H:%M:%S')
        handler.setFormatter(formatter)
logging.getLogger('oas').setLevel('DEBUG')

app = django.core.handlers.wsgi.WSGIHandler()

