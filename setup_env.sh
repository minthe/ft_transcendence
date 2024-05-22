#!bin/bash
echo "test"
#  create .env files for public and secret if not there
if [ -e ".env" ]; then
    echo "File '.env' already exists."
else
    # Create the file
    touch ".env"
    echo "File '.env' has been created."
fi

if [ -e "ms_hashi_vault/vault_store_secrets/.env" ]; then
    echo "File 'ms_hashi_vault/vault_store_secrets/.env' already exists."
else
    # Create the file
    touch "ms_hashi_vault/vault_store_secrets/.env"
    echo "File 'ms_hashi_vault/vault_store_secrets/.env' has been created."
fi


# update .env from gist
if grep -q "^GIST_URL=" .env; then
	gist_url_public=$(grep "^GIST_URL=" .env | cut -d= -f2- | tr -d "'")
	#echo "$gist_url_public"
	git clone $gist_url_public temp_folder_public
	cp -f temp_folder_public/public_env .env || { echo "Failed to copy Gist contents to .env"; exit 1; }
	rm -rf temp_folder_public
	#echo "GIST_URL='$gist_url_value'" >> ".env"
else
	echo "GIST_URL='https://gist.github.com/...'" >> .env
	echo "Please update the GIST_URL in .env"
	exit 1
fi



if grep -q "^GIST_URL=" ms_hashi_vault/vault_store_secrets/.env; then
	gist_url_secret=$(grep "^GIST_URL=" ms_hashi_vault/vault_store_secrets/.env | cut -d= -f2- | tr -d "'")
	git clone $gist_url_secret temp_folder_secret
	cp -f temp_folder_secret/secret_env ms_hashi_vault/vault_store_secrets/.env || { echo "Failed to copy Gist contents to .env"; exit 1; }
	rm -rf temp_folder_secret
	echo "GIST_URL='$gist_url_value'" >> "ms_hashi_vault/vault_store_secrets/.env"
else
	echo "GIST_URL='https://gist.github.com/...'" >> ms_hashi_vault/vault_store_secrets/.env
	echo "Please update the GIST_URL in ms_hashi_vault/vault_store_secrets/.env"
	exit 1
fi

# privat
# GIST_URL=''https://gist.github.com/2e06c1c4c25eff76c9ba35e9b19d7900.git'

#public
# GIST_URL='https://gist.github.com/d9e4d905934f98a7c5628c325065254d.git'