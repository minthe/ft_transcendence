# Use a base image with Vault pre-installed
# Use a base image with the required OS and dependencies for HashiCorp Vault
FROM python:3-alpine

# Set the environment variables
ENV VAULT_VERSION=1.9.3
ENV VAULT_ADDR=http://127.0.0.1:8200

COPY config.hcl .

# Download and install Vault
RUN apk add --no-cache curl
RUN curl -o vault.zip -L https://releases.hashicorp.com/vault/${VAULT_VERSION}/vault_${VAULT_VERSION}_linux_amd64.zip && \
    unzip vault.zip && \
    mv vault /usr/local/bin/ && \
    rm vault.zip

# RUN mkdir secret
# Expose the port Vault listens on
EXPOSE 8200

# Set the command to run Vault in server mode
CMD ["sh", "-c", "vault server -dev"]
