FROM python:3.7 AS build

WORKDIR /app
RUN pip install pip install torch==1.4.0+cpu torchvision==0.5.0+cpu -f https://download.pytorch.org/whl/torch_stable.html

COPY requirements.txt /app/
RUN pip install --user -r requirements.txt

FROM python:3.7-slim

COPY --from=build /root/.local /root/.local
WORKDIR /app
ENV PATH=$PATH:/root/.local/bin
COPY app /app
COPY app/onmt_server_conf.json /app/onmt_server_conf.json

RUN mkdir -p /app/models
ENTRYPOINT ["/usr/bin/dumb-init", "--"]
