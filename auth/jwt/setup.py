from setuptools import setup, find_packages

setup(
    name='ft_jwt_validation',
    version='1.0.1',
    author='vfuhlenb',
    description='A Django app for JWT validation',
    packages=find_packages(),
    install_requires=[
        'Django>=5.0',
    ],
)