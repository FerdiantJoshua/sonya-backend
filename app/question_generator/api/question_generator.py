import json

from fastapi import Response, status
import requests

from ..preprocess.prepare_free_input import prepare_featured_input
from .logger import Logger

INVALID_PARAMETER_MESSAGE = 'Masukan parameter tidak sesuai.'
logger = Logger()


class QuestionGenerator:
    def __init__(self, tokenizer_url: str, config_path: str, pos_url: str, ner_url: str, onmt_server_url: str):
        with open(config_path, 'r') as f_in:
            self.model_config = json.load(f_in)
        self.tokenizer_url = tokenizer_url
        self.pos_url = pos_url
        self.ner_url = ner_url
        self.onmt_server_url = onmt_server_url

        self.lower = self.model_config['lower']

    async def generate(self, text) -> Response:
        sentences = self._preprocess(text)
        model_id = self.model_config['models'][0]['id']
        payload = [{'id': model_id, 'src': sentence} for sentence in sentences]
        response = requests.post(
            self.onmt_server_url,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        predictions = [prediction['tgt'] for prediction in response.json()[0]]
        prediction = self._post_process(predictions)

        result = Response(
            json.dumps({'text': prediction}),
            status_code=status.HTTP_200_OK, media_type='application/json'
        )
        return result

    def _preprocess(self, text: str) -> [str]:
        preprocessed_sentences = prepare_featured_input(text, self.lower)
        return preprocessed_sentences

    def _post_process(self, sentences: [str]) -> str:
        return sentences
