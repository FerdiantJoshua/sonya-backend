from environs import Env

env = Env()
env.read_env()

API_CONFIG = {
    'development_host': env.str('DEVELOPMENT_HOST', '0.0.0.0'),
    'development_port': env.int('DEVELOPMENT_PORT', 21001),
    'pos_url': env.str('POS_URL'),
    'ner_url': env.str('NER_URL'),
    'onmt_server_host': env.str('ONMT_SERVER_HOST', '0.0.0.0'),
    'onmt_server_port': env.int('ONMT_SERVER_PORT', 21000),
    'onmt_server_url_root': env.str('ONMT_SERVER_URL_ROOT', '/question-generator'),
    'onmt_server_config': env.str('ONMT_SERVER_CONFIG'),
    'random_answer_entity_chance': env.float('RANDOM_ANSWER_ENTITY_CHANCE'),
    'log_level': env.log_level('LOG_LEVEL', 'INFO'),
}
