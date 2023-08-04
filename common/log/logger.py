# -*- coding: utf-8 -*-

import logging.config
import logging.handlers
import os
from typing import Dict

import common.config as config

FORMAT = '{%(name)s} {%(levelname)s} {pid:%(process)d} {%(module)s.%(funcName)s:%(lineno)d} >>> %(message)s'


def get_rotating_file_handler_config(file_name: str) -> Dict:
    return {
        'level': 'INFO',
        'class': 'logging.handlers.RotatingFileHandler',
        'formatter': 'file',
        'filename': f"{config.log_path}/{file_name}",
        'maxBytes': 1024 << 17,
        'backupCount': 10,
        'encoding': 'utf-8'
    }


def initialize():
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'console': {
                'format': FORMAT
            },
            'file': {
                'format': f'%(asctime)s {FORMAT}'
            },
        },
        'handlers': {
            'console': {
                'level': os.environ.get("log_level", "INFO").upper(),
                'class': 'logging.StreamHandler',
                'formatter': 'console'
            },
        },
        'loggers': {
            'root': {
                'handlers': ['console'],
                'level': os.environ.get("log_level", "INFO").upper(),
            }
        }
    }

    if config.environment != "local":
        os.makedirs(config.log_path, exist_ok=True)
        LOGGING['handlers']['file-log'] = get_rotating_file_handler_config('vb.log')
        LOGGING['loggers']["root"]['handlers'] = ['console', 'file-log']

    logging.config.dictConfig(LOGGING)
