#!bin/bash

current_host=$(hostname)

if grep -q '^CURRENT_HOST=' .env; then
    if [[ $(uname) == "Darwin" ]]; then
        sed -i '' "s/^CURRENT_HOST=.*/CURRENT_HOST='$current_host'/" .env
    else
        sed -i "s/^CURRENT_HOST=.*/CURRENT_HOST='$current_host'/" .env
    fi
else
    echo "CURRENT_HOST='$current_host'" >> .env
fi

if [[ $current_host == *"42wolfsburg"* || $current_host == *"localhost"* || $current_host == *"127.0."* || $current_host == *"192.168."* ]]; then
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout "./.ssl/privkey_$current_host.pem" -out "./.ssl/fullchain_$current_host.pem" \
        -subj "/CN=$current_host"
fi
