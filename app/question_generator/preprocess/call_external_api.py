import json

from environs import Env
import requests

env = Env()
env.read_env()


POS_URL = env.str('POS_URL')
NER_URL = env.str('NER_URL')

def get_pos_tag(text):
    payload = json.dumps({'text': text})
    headers = {
        "content-type": "application/json",
        "x-api-key": ""
        }

    res = requests.request("POST", POS_URL, headers=headers, data=payload)
    data = res.json()

    return data

def get_ner(text):
    payload = json.dumps({'text': text})
    headers = {
        "content-type": "application/json",
        "x-api-key": ""
        }

    res = requests.request("POST", NER_URL, headers=headers, data=payload)
    data = res.json()

    return data
