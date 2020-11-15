import random
from typing import List, Tuple

import numpy as np

from .call_external_api import get_ner, get_pos_tag
from .features import NONE_NER_POS, is_end_punctuations, create_ner_tensor, create_postags_tensor
from ..util.file_handler import print_input_along_feature, FEAT_SEP
from ..util.tokenizer import tokenize, normalize_string


class ExternalAPIInvocationError(Exception):
    pass


def sentenize(tokenized_input: List, entities: List, postags: List) -> Tuple[List, List, List]:
    final_sentences = []
    final_entities = []
    final_postags = []

    temp_sent = []
    temp_entities = []
    temp_postag = []
    for i in range(len(tokenized_input)):
        temp_sent.append(tokenized_input[i])
        temp_entities.append(entities[i])
        temp_postag.append(postags[i])
        if is_end_punctuations(tokenized_input[i]):
            final_sentences.append(temp_sent.copy())
            final_entities.append(temp_entities.copy())
            final_postags.append(temp_postag.copy())
            temp_sent = []
            temp_entities = []
            temp_postag = []
    return final_sentences, final_entities, final_postags


def get_entities_position_group(entities) -> List[Tuple[int, int]]:
    entities_position_group = []
    entity_position_group = []
    prev_ne = NONE_NER_POS
    i = -1
    for i in range(len(entities)):
        if entities[i] != NONE_NER_POS and prev_ne == NONE_NER_POS:
            entity_position_group.append(i)
        elif entities[i] != prev_ne and prev_ne != NONE_NER_POS:
            entity_position_group.append(i - 1)
            assert len(entity_position_group) == 2, entities
            entities_position_group.append(tuple(entity_position_group))
            entity_position_group = [] if entities[i] == NONE_NER_POS else [i]
        prev_ne = entities[i]
    if i >= 0 and prev_ne != NONE_NER_POS:
        entity_position_group.append(i)
        entities_position_group.append(tuple(entity_position_group))
    return entities_position_group


def _generate_random_start_end_idx(len_list: int, seed=42) -> Tuple[int, int]:
    random.seed(seed)
    start_idx = random.randint(0, len_list - 2)
    length = random.randint(2, 6)
    end_idx = min(start_idx + length, len_list)
    start_end_idx = (start_idx, end_idx)
    return start_end_idx


def get_random_answer_loc(tokenized_input: List[str], entities: List[str], entity_chance=0.8, seed=42) -> List[List[str]]:
    random.seed(seed)
    entities_position_group = get_entities_position_group(entities)
    get_from_entity = random.random()
    if len(entities_position_group) > 0 and get_from_entity <= entity_chance:
        answer_loc = entities_position_group[random.randint(0, len(entities_position_group) - 1)]
    else:
        answer_loc = _generate_random_start_end_idx(len(tokenized_input), seed=seed)
    is_answer = ['0' if i not in range(answer_loc[0], answer_loc[1] + 1) else '1' for i in range(len(tokenized_input))]
    return [is_answer]


def get_all_answer_locs(tokenized_input: List[str], entities: List[str], seed=42, **kwargs) -> List[List[str]]:
    list_of_is_answer = []
    answer_locs = get_entities_position_group(entities)
    answer_locs.append(_generate_random_start_end_idx(len(tokenized_input), seed=seed))
    for answer_loc in answer_locs:
        list_of_is_answer.append(['0' if i not in range(answer_loc[0], answer_loc[1] + 1) else '1' for i in range(len(tokenized_input))])
    return list_of_is_answer


def _create_is_cased_feature(tokenized_sent: list) -> List[str]:
    is_cased = []
    for j in range(len(tokenized_sent)):
        is_cased.append(
            '1' if j < len(tokenized_sent) and any(c.isupper() for c in tokenized_sent[j]) \
                else '0'
        )
    return is_cased


N_QUESTIONS_TO_FUNC = {
    'min': get_random_answer_loc,
    'max': get_all_answer_locs
}
def prepare_featured_input(input_text: str, lower: bool = False, n_questions: str = 'min', random_answer_entity_chance: float = 0.8, seed : int = 42) -> List[str]:
    if n_questions.lower() not in N_QUESTIONS_TO_FUNC:
        raise ValueError(f'n_answers value must be one of the following: {list(N_QUESTIONS_TO_FUNC)}')

    is_answer_sents = []
    is_cased_sents = []
    try:
        entities = get_ner(input_text)['entities']
        postags = get_pos_tag(input_text)['postags']
    except TimeoutError as e:
        raise ExternalAPIInvocationError('Unable to invoke the NE and/or Pos Tag API. Please check your VPN or your internet connection.') from e
    tokenized_input = tokenize(normalize_string(input_text))
    entities = create_ner_tensor(tokenized_input, entities, ner_textdict=None, return_in_tensor=False)
    postags = create_postags_tensor(tokenized_input, postags, postags_textdict=None, return_in_tensor=False)
    tokenized_sents, entity_sents, postag_sents = sentenize(tokenized_input, entities, postags)
    i = 0
    while i < len(tokenized_sents):
        is_cased = _create_is_cased_feature(tokenized_sents[i])
        list_of_answer_locs = N_QUESTIONS_TO_FUNC[n_questions](tokenized_sents[i], entity_sents[i], seed=seed, entity_chance=random_answer_entity_chance)

        additional_sentences = 0
        for j in range(len(list_of_answer_locs)):
            is_answer = list_of_answer_locs[j]
            is_answer_sents.append(is_answer)
            is_cased_sents.append(is_cased)
            if j > 0:
                tokenized_sents.insert(i, tokenized_sents[i])
                entity_sents.insert(i, entity_sents[i])
                postag_sents.insert(i, postag_sents[i])
                additional_sentences += 1

        i += 1 + additional_sentences

    tokenized_sents = np.array(tokenized_sents)

    # YES, DIRTY CODE. But have no choice to force the numpy to keep the input as array-of-list instead of pure array
    is_answer_sents = np.array(is_answer_sents+[[]])[:-1]
    is_cased_sents = np.array(is_cased_sents+[[]])[:-1]
    entity_sents = np.array(entity_sents+[[]])[:-1]
    postag_sents = np.array(postag_sents+[[]])[:-1]

    is_answer_sents = np.expand_dims(is_answer_sents, axis=-1)
    is_cased_sents = np.expand_dims(is_cased_sents, axis=-1)
    entity_sents = np.expand_dims(entity_sents, axis=-1)
    postag_sents = np.expand_dims(postag_sents, axis=-1)

    if lower:
        features = np.concatenate((is_answer_sents, is_cased_sents, entity_sents, postag_sents), axis=-1)
    else:
        features = np.concatenate((is_answer_sents, entity_sents, postag_sents), axis=-1)

    output = []
    for i in range(len(tokenized_sents)):
        if lower:
            output.append((print_input_along_feature(tokenized_sents[i], features[i]) + '\n').lower())
        else:
            output.append((print_input_along_feature(tokenized_sents[i], features[i]) + '\n'))
    return output


def sent_tokenize(input_text: str) -> List[List[str]]:
    tokenized_sents = []
    tokenized_input = tokenize(normalize_string(input_text))
    sentence = []
    for token in tokenized_input:
        sentence.append(token)
        if is_end_punctuations(token):
            tokenized_sents.append(sentence.copy())
            sentence = []
    return tokenized_sents


def prepare_simple_input(input_text: str) -> List[str]:
    tokenized_sents = sent_tokenize(input_text)
    output = []
    for sentence in tokenized_sents:
        output.append(' '.join(sentence) + '\n')
    return output


def convert_answer_loc_to_string(featured_input: str) -> str:
    answer_as_text = ''
    featured_tokens = featured_input.split()
    for featured_token in featured_tokens:
        token, is_answer = featured_token.split(FEAT_SEP)[:2]
        answer_as_text += ' ' + token if int(is_answer) else ''
    return answer_as_text[1:]
