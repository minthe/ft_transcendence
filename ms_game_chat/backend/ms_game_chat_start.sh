#!/bin/sh

python manage.py makemigrations
python manage.py migrate
WEBSERVER='python manage.py runserver 0.0.0.0:6969'