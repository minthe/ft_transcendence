#!/bin/sh

envsubst '$CURRENT_HOST' < /nginx.conf > /etc/nginx/nginx.conf
nginx -g 'daemon off;'