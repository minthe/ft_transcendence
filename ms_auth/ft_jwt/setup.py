import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="ft_jwt",
	version="0.0.17",
	author="vfuhlenb",
	author_email="minh.tee@gmail.com",
	description="A Python implementation of JSON Web Tokens (JWT) for authentication and authorization using a symmetric secret key and HMAC-SHA256.",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/minthe/ft_transcendence/blob/main/auth/ft_jwt/ft_jwt/ft_jwt.py",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)