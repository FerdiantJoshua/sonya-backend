import json
from typing import Dict, List

from fastapi import Response, status
import requests

from ..preprocess.prepare_free_input import prepare_featured_input, convert_answer_loc_to_string
from .logger import Logger

INVALID_PARAMETER_MESSAGE = 'Masukan parameter tidak sesuai.'
logger = Logger()


class QuestionGenerator:
    def __init__(self, config_path: str, pos_url: str, ner_url: str, onmt_server_url: str, random_answer_entity_chance: float = 0.8) -> None:
        with open(config_path, 'r') as f_in:
            self.model_config = json.load(f_in)
        self.pos_url = pos_url
        self.ner_url = ner_url
        self.onmt_server_url = onmt_server_url
        self.random_answer_entity_chance = random_answer_entity_chance

        self.lower = self.model_config['lower']

    async def generate(self, text: str, n_questions: str) -> Response:
        sentences = self._preprocess(text, n_questions)
        model_id = self.model_config['models'][0]['id']
        payload = [{'id': model_id, 'src': sentence} for sentence in sentences]
        response = requests.post(
            self.onmt_server_url,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        predictions = [prediction['tgt'] for prediction in response.json()[0]]
        prediction = self._post_process(predictions, sentences)

        result = Response(
            json.dumps({'text': prediction}),
            status_code=status.HTTP_200_OK, media_type='application/json'
        )
        return result

    def _preprocess(self, text: str, n_questions: str) -> List[str]:
        text = text.replace('\n', '')
        preprocessed_sentences = prepare_featured_input(text, lower=self.lower, n_questions=n_questions,
                                                        random_answer_entity_chance=self.random_answer_entity_chance)
        return preprocessed_sentences

    def _post_process(self, questions: List[str], featured_inputs: List[str]) -> List[Dict]:
        assert len(questions) == len(featured_inputs)
        final_output = []
        question_and_answer = {}
        for i in range(len(questions)):
            question = questions[i]
            featured_input = featured_inputs[i]
            logger.log(logger.DEBUG, featured_input.strip())
            question_and_answer['question'] = question.strip()
            question_and_answer['answer'] = convert_answer_loc_to_string(featured_input)
            final_output.append(question_and_answer)
            question_and_answer = {}
        return final_output
