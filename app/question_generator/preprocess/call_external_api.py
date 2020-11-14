import http.client
import json
from environs import Env

env = Env()
env.read_env()


POS_URL = env.str('POS_URL')
NER_URL = env.str('NER_URL')

def get_pos_tag(text):
    conn = http.client.HTTPConnection(POS_URL)
    payload = json.dumps({'text': text})
    headers = {
        "content-type": "application/json",
        "x-api-key": ""
        }

    conn.request('POST', '/', payload, headers)
    res = conn.getresponse()
    data = json.loads(res.read().decode('utf-8'))

    return data

def get_ner(text):
    conn = http.client.HTTPConnection(NER_URL)
    payload = json.dumps({'text': text})
    headers = {
        "content-type": "application/json",
        "x-api-key": ""
        }

    conn.request('POST', '/', payload, headers)
    res = conn.getresponse()
    data = json.loads(res.read().decode('utf-8'))

    return data
