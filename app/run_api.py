import uvicorn

from question_generator.api.config import API_CONFIG
from question_generator.api.main import question_generator_api

DEVELOPMENT_HOST = API_CONFIG['development_host']
DEVELOPMENT_PORT = API_CONFIG['development_port']


if __name__ == '__main__':
    uvicorn.run(question_generator_api, host=DEVELOPMENT_HOST, port=DEVELOPMENT_PORT)
