#!/bin/bash
PYTHONPATH="$PYTHONPATH:/home/christophe/.ve_config/oasserver/lib/python2.7/site-packages:/opt/google_appengine:/opt/google_appengine/lib/django_1_3" python server/manage.py syncdb


