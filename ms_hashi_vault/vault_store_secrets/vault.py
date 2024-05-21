import hvac
from dotenv import dotenv_values

def write_secret_to_vault(key, value):
    # Initialize the Vault client
    vault_client = hvac.Client(url='http://vault:8200', token='root')

    # Define the path where you want to store the secret
    secret_path = 'secret/data/{}'.format(key)
    print(secret_path)

    # Prepare the data payload
    data = {'data': {key: value}}

    # Write the secret to Vault
    response = vault_client.write(secret_path, **data)

    # Check if the write operation was successful
    if response and response.get('data') and response['data'].get('created'):
        print(f"Secret '{key}' successfully written to Vault at '{secret_path}'")
    else:
        print("Failed to write secret to Vault")

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

# Example usage:
secret_value = read_secret_from_vault("POSTGRES_PASSWORD")
print(secret_value)


# Load key-value pairs from the .env file
env_vars = dotenv_values('.env')

# Write each key-value pair to Vault
for key, value in env_vars.items():
    write_secret_to_vault(key, value)

secret_path = 'secret/data/CURRENT_HOST'
secret_data = read_secret_from_vault(secret_path)
print("Secret data:", secret_data)
secret_data = read_secret_from_vault('POSTGRES_PASSWORD')
print("Secret data:", secret_data)
secret_data = read_secret_from_vault('POSTGRES_PORT')
print("Secret data:", secret_data)
