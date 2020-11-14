FROM python:3.7 AS build

WORKDIR /app
COPY requirements.txt /app/

RUN pip install --user -r requirements.txt

FROM python:3.7-slim

RUN apt-get update && apt-get install -y curl dumb-init git gnupg python3-dev libev-dev
RUN export GCSFUSE_REPO=gcsfuse-stretch && \
    echo "deb http://packages.cloud.google.com/apt $GCSFUSE_REPO main" >> /etc/apt/sources.list.d/gcsfuse.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -

RUN apt update && apt install -y libc6 gcsfuse

COPY --from=build /root/.local /root/.local
WORKDIR /app
ENV PATH=$PATH:/root/.local/bin
COPY app /app
COPY app/onmt_server_conf.example.json /app/onmt_server_conf.json
RUN sed -i 's/.\/models\/onmt/\/app\/models/g' /app/onmt_server_conf.json

RUN mkdir -p /app/models
ENTRYPOINT ["/usr/bin/dumb-init", "--"]

CMD python run_onmt_server.py
