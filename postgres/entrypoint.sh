#!/bin/bash

# Execute set_env.sh script#

./create_vault_cli.sh
./set_env.sh

# Start PostgreSQL
exec "$@"