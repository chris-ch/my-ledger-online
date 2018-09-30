#!/usr/bin/env bash

chmod 755 /startup/*.bash

# Gives more time to Postgres to start: to be replaced with a waiting script
# as indicated here: https://docs.docker.com/compose/startup-order
sleep 2

python /startup/manage.py migrate

python /startup/manage.py runserver 0.0.0.0:8000
