#!/bin/bash

echo "Executing set_env.sh script..."

postgres_user=$(vault read -format=json secret/data/POSTGRES_USER | jq -r '.data.data.POSTGRES_USER')

# postgres_user=$(echo "$postgres_user" | awk '{$1=$1};1')
postgres_password=$(vault read -format=json secret/data/POSTGRES_PASSWORD | jq -r '.data.data.POSTGRES_PASSWORD')
# postgres_password=$(echo "$postgres_passwword" | awk '{$1=$1};1')
postgres_port=$(vault read -format=json secret/data/POSTGRES_PORT | jq -r '.data.data.POSTGRES_PORT')
# postgres_port=$(echo "$postgres_port" | awk '{$1=$1};1')
postgres_db=$(vault read -format=json secret/data/POSTGRES_DB | jq -r '.data.data.POSTGRES_DB')
# postgres_db=$(echo "$postgres_db" | awk '{$1=$1};1')

echo "Retrieved secrets from Vault:"
# echo "$(vault read -format=json secret/data/POSTGRES_USER | jq -r '.data.data.POSTGRES_USER')"
# echo "test"
echo "POSTGRES_USER: $postgres_user"
echo "POSTGRES_PASSWORD: $postgres_password"
echo "POSTGRES_PORT: $postgres_port"
echo "POSTGRES_DB: $postgres_db"

export POSTGRES_USER="$postgres_user"
export POSTGRES_PASSWORD="$postgres_password"
export POSTGRES_PORT="$postgres_port"
export POSTGRES_DB="$postgres_db"
echo "Environment variables set successfully."

# Additional debugging output
echo "----------------- Current environment variables: --------------------"
env
