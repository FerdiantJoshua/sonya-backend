from enum import Enum
import json

from fastapi import FastAPI, Request, Response, status
from pydantic import BaseModel

from .config import API_CONFIG
from .logger import Logger
from .question_generator import QuestionGenerator
from .validator import validate_and_log, HTTP_500_ERROR_MESSAGE

logger = Logger()


class RequestBody(BaseModel):
    text: str


def create_app(tokenizer_url: str, onmt_model_config_path: str, pos_url: str, ner_url: str, onmt_server_url: str):
    app = FastAPI()

    question_generator = QuestionGenerator(tokenizer_url, onmt_model_config_path, pos_url, ner_url, onmt_server_url)

    @app.post('/')
    @validate_and_log()
    async def index(request_body: RequestBody, request: Request):
        body = request_body.dict()
        text = body['text']

        response = await question_generator.generate(text)

        return response

    return app


tokenizer_url = API_CONFIG['tokenizer_url']
pos_url = API_CONFIG['pos_url']
ner_url = API_CONFIG['ner_url']
onmt_server_host = API_CONFIG['onmt_server_host']
onmt_server_port = API_CONFIG['onmt_server_port']
onmt_server_url_root = API_CONFIG['onmt_server_url_root']
onmt_model_config_path = API_CONFIG['onmt_server_config']
onmt_server_url = f'http://{onmt_server_host}:{onmt_server_port}{onmt_server_url_root}/translate'

logger.log(logger.INFO, f'tokenizer_url: {tokenizer_url}')
logger.log(logger.INFO, f'pos_url: {pos_url}')
logger.log(logger.INFO, f'ner_url: {ner_url}')
logger.log(logger.INFO, f'onmt_server_url: {onmt_server_url}')

question_generator_api = create_app(tokenizer_url, onmt_model_config_path, pos_url, ner_url, onmt_server_url)
