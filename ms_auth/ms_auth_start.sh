#!/bin/sh

echo "DEBUG is set to: $DEBUG"

if [ "$DEBUG" = "True" ]; then
    echo "Debug mode is on"
	echo "Starting with django runserver"
	WEBSERVER='python manage.py runserver 0.0.0.0:8000'
else
    echo "Debug mode is off"
	echo "Starting with daphne"
	WEBSERVER='daphne -b 0.0.0.0 -p 8000 django_project.asgi:application'
fi

python manage.py makemigrations
python manage.py migrate
$WEBSERVER