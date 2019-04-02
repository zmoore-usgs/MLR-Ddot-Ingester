# MLR-Ddot-Ingester
[![Build Status](https://travis-ci.org/USGS-CIDA/MLR-Ddot-Ingester.svg?branch=master)](https://travis-ci.org/USGS-CIDA/MLR-Ddot-Ingester)
[![Coverage Status](https://coveralls.io/repos/github/USGS-CIDA/MLR-Ddot-Ingester/badge.svg)](https://coveralls.io/github/USGS-CIDA/MLR-Ddot-Ingester)

This project has been built and tested with python 3.6.x. To build the project locally you will need
python 3 and virtualenv installed.
```bash
% virtualenv --python=python3 env
% env/bin/pip install -r requirements.txt
```
To run the tests:
```bash
env/bin/python -m unittest
```

To run the application locally execute the following:
```bash
% env/bin/python app.py
```

The swagger documentation can then be accessed at http://127.0.0.1:5000/api (when running locally using the above command).

Default configuration variables can be overridden be creating a .env file. For instance to turn debug on, 
you will want to create an .env with the following:
```python
DEBUG = True
```

For local development, you will need to provide a JWT token to the service. This can be done through the Swagger documents by
clicking the Authorize button and entering 'Bearer your.jwt.token'. 

You can use a valid JWT token generated by another service. You will need to set it's JWT_PUBLIC_KEY to the public
key used to generate the token, as well as the JWT_DECODE_AUDIENCE (if any) and the JWT_ALGORITHM (if different than
RS256). If you don't want to verify the cert on this service, set AUTH_CERT_PATH to False.

Alternatively, you can generate your own token by using the python package jwt. In the python interpreter, do the following
```python
import jwt
jwt.encode({'authorities': ['one_role', 'two_role']}, 'secret', algorithm='HS256')
```
The output of this command will be the token that you can use. You will need to set JWT_SECRET_KEY to 'secret' in your local .env file. 
See http://flask-jwt-simple.readthedocs.io/en/latest/options.html for the other options that you can use.

## Running with Docker 
This application can also be run locally using the docker container built during the build process, though this does not allow the application to be run in debug mode. The included `docker-compose` file has 2 profiles to choose from when running the application locally:

1. mlr-ddot-ingester: This is the default profile which runs the application as it would be in our cloud environment. This is not recommended for local development as it makes configuring connections to other services running locally on your machine more difficult.
2. mlr-ddot-ingester-local-dev: This is the profile which runs the application as it would be in the mlr-local-dev project, and is configured to make it easy to replace the mlr-ddot-ingester instance in the local-dev project with this instance. It is run the same as the `mlr-ddot-ingester` profile, except it uses the docker host network driver.

Before any of these options are able to be run you must also generate certificates for this application to serve using the `create_certificates` script in the `docker/certificates` directory. Additionally, this service must be able to connect to a running instance of Water Auth when starting, and it is recommended that you use the Water Auth instance from the `mlr-local-dev` project to accomplish this. In order for this application to communicate with any downstream services that it must call, including Water Auth, you must also place the certificates that are being served by those services into the `docker/certificates/import_certs` directory to be imported into the Python CA Certificates of the running container.

To build and run the application after completing the above steps you can run: `docker-compose up --build {profile}`, replacing `{profile}` with one of the options listed above.

The swagger documentation can then be accessed at http://127.0.0.1:6028/api