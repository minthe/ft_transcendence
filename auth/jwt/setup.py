from setuptools import setup, find_packages

setup(
    name='ft_jwt_validation',
    version='1.0.0',
    author='vfuhlenb',
    description='A Django app for JWT validation',
    packages=find_packages(),
    install_requires=[
        'hashlib',
        'base64',
        'hmac',
        'json',
    ],
)