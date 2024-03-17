#!bin/bash

if [ ! -d "./.cert" ]; then
    mkdir .cert
fi

if grep -q "^CURRENT_HOST=" .env; then
	current_host=$(grep "^CURRENT_HOST=" .env | cut -d= -f2- | tr -d "'")
else
	current_host=$(hostname)
	echo "CURRENT_HOST='$current_host'" >> .env
fi

if [[ $current_host != *"playpong"* ]]; then
	openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
		-keyout "./.cert/privkey_$current_host.pem" -out "./.cert/fullchain_$current_host.pem" \
		-subj "/CN=$current_host"
fi

directory="game_chat"
if [ -z "$(ls -A $directory)" ]; then
	git submodule init $directory
	git submodule update $directory
fi

# Update the IP address for duckdns
if [[ $current_host == *"playpong"* ]]; then
	echo url="https://www.duckdns.org/update?domains=playpong&token=e3cea228-d11d-4e36-a4bc-5b184f95e55a&ip=" | curl -k -o setup.log -K -
fi
