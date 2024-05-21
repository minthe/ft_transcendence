# microservice1/app.py

import os
import hvac
import time as t

# Step 1: Generate Secret (example function)
def generate_secret():
    # Generate a random secret (example)
    return "random_secret_here"

def write_secret_to_vault(secret):
    vault_client = hvac.Client(url='http://localhost:8200', token='root')
    secret_path = 'secret/data/my_secret'
    vault_client.write(secret_path, data={'secret_key': secret})

def read_secret_from_vault():
    vault_client = hvac.Client(url='http://localhost:8200', token='root')
    secret_path = 'secret/data/my_secret'
    response = vault_client.read(secret_path)
    if response is not None and 'data' in response:
        return response['data']
    else:
        return None


def main():
    generated_secret = generate_secret()
    print("generated secret: ")
    print(generate_secret)
    print("\n")
    write_secret_to_vault(generated_secret)
    stored_secret = read_secret_from_vault()
    print("retrieved secret from hashi vault microservice: ")
    print(stored_secret)
    print("\n")
    while 2:
        t.sleep(10)

if __name__ == "__main__":
    main()
