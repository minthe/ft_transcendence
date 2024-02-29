#!/bin/sh

# Substitute environment variables in nginx.conf.template and create nginx.conf
envsubst '$CURRENT_HOST' < /nginx.conf.template > /etc/nginx/nginx.conf
nginx -g 'daemon off;'