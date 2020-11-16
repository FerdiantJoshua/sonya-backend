FROM python:3.7 AS build

WORKDIR /app
RUN pip install --user torch==1.4.0+cpu torchvision==0.5.0+cpu -f https://download.pytorch.org/whl/torch_stable.html

COPY requirements.txt /app/
RUN pip install --user -r requirements.txt

FROM python:3.7-slim

COPY --from=build /root/.local /root/.local
WORKDIR /app
ENV PATH=$PATH:/root/.local/bin
COPY app /app
