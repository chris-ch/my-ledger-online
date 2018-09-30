#!/usr/bin/env bash



python /startup/manage.py migrate

python /startup/manage.py runserver 0.0.0.0:8000
