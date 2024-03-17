#!bin/bash

source .env

if [ ! -d "./.cert" ]; then
    mkdir .cert
fi

if grep -q "^CURRENT_HOST=" .env; then
	current_host=$(grep "^CURRENT_HOST=" .env | cut -d= -f2- | tr -d "'")
else
	current_host=$(hostname)
	echo -e "\nCURRENT_HOST='$current_host'" >> .env
fi

if [[ $CURRENT_HOST != *"playpong"* ]]; then
	openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
		-keyout "./.cert/privkey_$CURRENT_HOST.pem" -out "./.cert/fullchain_$CURRENT_HOST.pem" \
		-subj "/CN=$CURRENT_HOST"
fi

directory="game_chat"
if [ -z "$(ls -A $directory)" ]; then
	git submodule init $directory
	git submodule update $directory
fi

# Update the IP address for duckdns
if [[ "$CURRENT_HOST" != *"localhost"*  && "$CURRENT_HOST" == *"duckdns.org"* ]]; then
	echo "Updating IP address for $CURRENT_HOST" > status_duckdns.log
	echo url="https://www.duckdns.org/update?domains=$CURRENT_HOST&token=$DUCKDNS_TOKEN" | curl -k -K - >> status_duckdns.log
fi
