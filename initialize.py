from common.log import logger
from datasource.config import rdbms_instance
from datasource.rdbms.entities import CharacterModel


def initialize():
    logger.initialize()
