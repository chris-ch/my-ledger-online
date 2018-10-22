#!/usr/bin/env bash

chmod 755 /startup/*.bash

# Gives more time to Postgres to start: to be replaced with a waiting script
# as indicated here: https://docs.docker.com/compose/startup-order
#sleep 2

until python /startup/manage.py check; do sleep 1; done; python /startup/manage.py migrate

#python /startup/manage.py createsuperuser --username oas --no-input --email oas@nowhere.ch

python /startup/manage.py runserver 0.0.0.0:8000
