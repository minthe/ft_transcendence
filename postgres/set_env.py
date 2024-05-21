import hvac
import os
from dotenv import dotenv_values

def read_secret_from_vault(key):
    # Construct the secret path using the key
    secret_path = f"secret/data/{key}"
    
    # Initialize the Vault client
    vault_client = hvac.Client(url='http://vault:8200', token='root')

    # Read the secret from Vault
    response = vault_client.read(secret_path)

    # Check if the read operation was successful
    if response and response.get('data') and response['data'].get('data'):
        # Extract and return the secret data
        secret_data = response['data']['data']
        # Return the value corresponding to the given key
        return secret_data.get(key)
    else:
        print(f"Failed to read secret from Vault at '{secret_path}'")
        return None

os.environ['POSTGRES_USER'] = read_secret_from_vault('POSTGRES_USER')
os.environ['POSTGRES_PASSWORD'] = read_secret_from_vault('POSTGRES_PASSWORD')
os.environ['POSTGRES_DB'] = read_secret_from_vault('POSTGRES_DB')
os.environ['POSTGRES_PORT'] = read_secret_from_vault('POSTGRES_PORT')