FROM python:3.6-alpine as build

# Add build dependencies (See: https://github.com/gliderlabs/docker-alpine/issues/458)
RUN apk add -U --no-cache gcc build-base linux-headers ca-certificates python3-dev libffi-dev openssl-dev py3-virtualenv

COPY --chown=1000:1000 requirements.txt /build/requirements.txt

WORKDIR /build

RUN virtualenv --python=python3.6 env
RUN env/bin/pip install -r requirements.txt && env/bin/pip install wheel

COPY --chown=1000:1000 README.md /build/README.md
COPY --chown=1000:1000 *.py /build/
COPY --chown=1000:1000 tests /build/tests

RUN env/bin/python -m unittest && env/bin/python setup.py bdist_wheel

FROM cidasdpdasartip.cr.usgs.gov:8447/mlr-python-base-docker:latest
LABEL maintainer="gs-w_eto_eb_federal_employees@usgs.gov"

ENV listening_port=6028
ENV protocol=https
ENV oauth_server_token_key_url=https://test.gov/oauth/token_key
ENV authorized_roles=test_default

COPY --chown=1000:1000 --from=build /build/dist/*.whl .

RUN pip3 install --no-cache-dir --quiet --user ./*.whl

HEALTHCHECK CMD curl -k ${protocol}://127.0.0.1:${listening_port}/version | grep -q "\"artifact\": \"${artifact_id}\"" || exit 1
