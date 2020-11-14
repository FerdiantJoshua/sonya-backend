MAKEFILE_TARGET := $(firstword $(MAKECMDGOALS))
BIND ?= 0.0.0.0:30000
N_WORKER ?= 4

init:
  mkdir -p models/
	cp .env.example .env
	cp app/onmt_server_conf.example.json app/onmt_server_conf.json
	pip install pip install torch==1.4.0+cpu torchvision==0.5.0+cpu -f https://download.pytorch.org/whl/torch_stable.html
	pip install -r requirements.txt

run_onmt_server:
	python app/run_onmt_server.py

run_api_dev:
	python app/run_api.py

run_api_prod:
	gunicorn app.normalizer.api.main:normalizer_api --bind=${BIND} -w ${N_WORKER} -k uvicorn.workers.UvicornWorker
