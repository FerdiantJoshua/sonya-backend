# SINGLETON REFERENCE: https://gist.github.com/huklee/cea20761dd05da7c39120084f52fcc7c
import json
from logging.handlers import TimedRotatingFileHandler
import logging
import os

from .config import API_CONFIG

LOG_LEVEL = API_CONFIG['log_level']


class SingletonType(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonType, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Logger(object, metaclass=SingletonType):
    CRITICAL = logging.CRITICAL
    FATAL = logging.FATAL
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    WARN = logging.WARN
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    NOTSET = logging.NOTSET
    _logger = None

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(LOG_LEVEL)
        formatter = logging.Formatter('%(asctime)s [%(levelname)s - %(filename)s:%(lineno)s] > %(message)s')

        dirname = './log'
        if not os.path.isdir(dirname):
            os.mkdir(dirname)

        fileHandler = TimedRotatingFileHandler(encoding='utf-8', filename=dirname + '/log_api', when='midnight')
        fileHandler.setFormatter(formatter)
        self._logger.addHandler(fileHandler)

        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(formatter)
        self._logger.addHandler(streamHandler)

        self._logger.debug('Generating new logger instance')

    def log(self, level:int, msg:any, *args, **kwargs):
        self._logger.log(level, msg, *args, **kwargs)
