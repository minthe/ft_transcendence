# JWT Authentication

A Python implementation of JSON Web Tokens (JWT) for authentication and authorization using a symmetric secret key and HMAC-SHA256.

## Features

- Generate JWT tokens with customizable expiration times
- Validate JWT tokens and verify their integrity using a symmetric secret key and HMAC-SHA256
- Extract user information (such as user ID 'sub') from JWT tokens

## Installation

You can install the package via pip:

```pip install ft_jwt```

## Usage

```python
from ft_jwt.ft_jwt import FT_JWT

# Create a JWT instance with your secret key

secret_key = 'your_secret_key'
ftjwt = FT_JWT(secret_key)

# Generate a token for a user

sub = '1'
token = jwt.createToken(sub)

# Validate a token

is_valid, message = ftjwt.validateToken(token)
if is_valid:
    print('Token is valid')
else:
    print(f'Token is invalid: {message}')

# Get the user ID from a token

user_id = ftjwt.getUserId(token)
print(f'User ID: {sub}')

# Use the decorator to validate against a JWT for a protected route

@ftjwt.token_required
def protected_route():
    # This function will be executed only if the token is valid
    # ...
```

# Contributing
Contributions are welcome! Please open an issue or submit a pull request.

# License
This project is licensed under the MIT License.