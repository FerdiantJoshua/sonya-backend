from functools import wraps
import json
import os
import time

from fastapi import Response, status

from .logger import Logger

_ALLOWED_API_KEY = ''
HTTP_500_ERROR_MESSAGE = 'Terjadi kesalahan internal pada peladen kami.'
logger = Logger()


def is_invalid_input(text):
    return 'typeof Object' in text


def validate_and_log():
    def decorator(function):
        @wraps(function)    # A little tweak for fastapi decorator
        async def wrapper(*args, **kwargs):
            body = kwargs['request_body'].dict()
            request = kwargs['request']
            log = {}

            x_api_key = request.headers.get('x-api-key')
            log['api_key'] = x_api_key
            log['ip'] = request.client
            log['user_agent'] = request.headers.get('User-Agent')
            log['method'] = request.method
            log['path'] = request.url.path
            log['request'] = body

            start = time.time()
            if x_api_key != _ALLOWED_API_KEY:
                response = Response(
                    json.dumps({'message': 'Unauthorized \'x-api-key\''}),
                    status_code=status.HTTP_401_UNAUTHORIZED, media_type='application/json'
                )
            elif is_invalid_input(body['text']):
                response = Response(
                    json.dumps({'message': 'Text masukan mengandung konten javascript sehingga tidak dapat diproses.'}),
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, media_type='application/json'
                )
            elif len(body['text']) == 0:
                response = Response(
                    json.dumps({'message': 'Text masukan kosong'}),
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, media_type='application/json'
                )
            else:
                try:
                    response = await function(*args, **kwargs)
                    log['response'] = response.body.decode('utf-8')
                except Exception as e:
                    fname = os.path.split(e.__traceback__.tb_frame.f_code.co_filename)[1]
                    err = '[ERROR] {}:{} {}'.format(fname, e.__traceback__.tb_lineno, e.__class__.__name__)
                    log['response'] = err
                    response = Response(
                        json.dumps({'message': HTTP_500_ERROR_MESSAGE}),
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, media_type='application/json'
                    )
            end = time.time()

            log['latency'] = f'{(end - start) * 1000:.4f}'
            log['status'] = response.status_code
            log['ip'] = request.headers.get('X-Forwarded-For', 'False IP')

            logger.log(logger.INFO, log)
            return response
        return wrapper
    return decorator
