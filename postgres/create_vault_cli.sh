#!/bin/sh

# Install necessary packages
apk add --no-cache curl jq unzip

# Set Vault version
VAULT_ADDR="http://vault:8200"
VAULT_VERSION=1.9.3
VAULT_TOKEN="root"

# Download Vault binary, unzip, move to /usr/local/bin, and cleanup
curl -o vault.zip -L "https://releases.hashicorp.com/vault/${VAULT_VERSION}/vault_${VAULT_VERSION}_linux_amd64.zip" && \
unzip vault.zip && \
mv vault /usr/local/bin/ && \
rm vault.zip && \

# Print success message and check installed Vault version
echo "Vault installed successfully" && \
vault --version

echo "hello test"
