#!/bin/sh

envsubst '$CURRENT_HOST' < /nginx.conf.template > /etc/nginx/nginx.conf
nginx -g 'daemon off;'