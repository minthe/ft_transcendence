#!/bin/sh

echo "DEBUG is set to: $DEBUG"

if [ "$DEBUG" = "true" ]; then
    echo "Debug mode is on"
	echo "Starting with django runserver"
	WEBSERVER='python manage.py runserver 0.0.0.0:6969'
else
    echo "Debug mode is off"
	echo "Starting with daphne"
	WEBSERVER='daphne -b 0.0.0.0 -p 6969 backend.asgi:application'
fi

python manage.py makemigrations
python manage.py migrate
$WEBSERVER