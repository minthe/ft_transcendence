#!bin/bash

current_host=$(hostname)

if [ ! -d "./.cert" ]; then
    mkdir .cert
fi

if grep -q "^CURRENT_HOST=" .env; then
    if grep -q "^CURRENT_HOST='localhost'" .env || [[ $current_host == *"42wolfsburg"* ]]; then
        openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
            -keyout "./.cert/privkey_localhost.pem" -out "./.cert/fullchain_localhost.pem" \
            -subj "/CN=$current_host"
    fi
else
    echo "CURRENT_HOST='localhost'" >> .env
fi

