#!bin/bash

# update .env from gist
if grep -q "^GIST_URL=" .env; then
	gist_url=$(grep "^GIST_URL=" .env | cut -d= -f2- | tr -d "'")
	git clone $gist_url temp_folder
	cp -f temp_folder/.env .env || { echo "Failed to copy Gist contents to .env"; exit 1; }
	rm -rf temp_folder
else
	echo "GIST_URL='https://gist.github.com/...'" >> .env
	echo "Please update the GIST_URL in .env"
	exit 1
fi

