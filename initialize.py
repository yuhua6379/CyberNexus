from common.log import logger
from datasource.rdbms import sqlite


def initialize():
    logger.initialize()
    sqlite.initialize()
