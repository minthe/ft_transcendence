#!bin/bash

source .env

if [ ! -d "./.cert" ]; then
    mkdir .cert
fi

# Generate a self-signed certificate for the current host
if grep -q "^CURRENT_HOST=" .env; then
	current_host=$(grep "^CURRENT_HOST=" .env | cut -d= -f2- | tr -d "'")
else
	current_host=$(hostname)
	echo -e "\nCURRENT_HOST='$current_host'" >> .env
fi
echo "$current_host"
if [[ "$current_host" != *"playpong"* ]]; then
	openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
		-keyout "./.cert/privkey_$current_host.pem" -out "./.cert/fullchain_$current_host.pem" \
		-subj "/CN=$current_host"
fi

# Update the IP address for duckdns
if [[ "$current_host" != *"localhost"*  && "$current_host" == *"duckdns.org"* ]]; then
	echo "Updating IP address for $current_host" > status_duckdns.log
	echo url="https://www.duckdns.org/update?domains=$current_host&token=$DUCKDNS_TOKEN" | curl -k -K - >> status_duckdns.log
fi