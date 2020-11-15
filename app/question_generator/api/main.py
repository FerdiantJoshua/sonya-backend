from enum import Enum

from fastapi import FastAPI, Request, Response, status
from pydantic import BaseModel

from .config import API_CONFIG
from .logger import Logger
from .question_generator import QuestionGenerator
from .validator import validate_and_log, HTTP_500_ERROR_MESSAGE

logger = Logger()


class NQuestions(Enum):
    min = 'min'
    max = 'max'

    def __repr__(self):
        return str(self.value)


class RequestBody(BaseModel):
    text: str
    n_questions: NQuestions = NQuestions.min


def create_app(onmt_model_config_path: str, pos_url: str, ner_url: str, onmt_server_url: str, random_answer_entity_chance: float):
    app = FastAPI()

    question_generator = QuestionGenerator(onmt_model_config_path, pos_url, ner_url, onmt_server_url, random_answer_entity_chance)

    @app.post('/')
    @validate_and_log()
    async def index(request_body: RequestBody, request: Request):
        body = request_body.dict()
        text = body['text']
        n_questions = body['n_questions']

        response = await question_generator.generate(text, n_questions.value)

        return response

    return app


pos_url = API_CONFIG['pos_url']
ner_url = API_CONFIG['ner_url']
onmt_server_host = API_CONFIG['onmt_server_host']
onmt_server_port = API_CONFIG['onmt_server_port']
onmt_server_url_root = API_CONFIG['onmt_server_url_root']
onmt_model_config_path = API_CONFIG['onmt_server_config']
onmt_server_url = f'http://{onmt_server_host}:{onmt_server_port}{onmt_server_url_root}/translate'
random_answer_entity_chance =  API_CONFIG['random_answer_entity_chance']

logger.log(logger.INFO, f'pos_url: {pos_url}')
logger.log(logger.INFO, f'ner_url: {ner_url}')
logger.log(logger.INFO, f'onmt_server_url: {onmt_server_url}')

question_generator_api = create_app(onmt_model_config_path, pos_url, ner_url, onmt_server_url, random_answer_entity_chance)
