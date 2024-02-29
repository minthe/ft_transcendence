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
