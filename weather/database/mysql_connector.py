import mysql.connector
from . import config
import logging

logger = logging.getLogger(__name__)

config = config.get_config()

class mysql_connector():
    mysql_connector_obj = None
    mysql_db = None

    def __init__(self):
        self.connect()
        logger.info("MySql Connection is initiated.")
        mysql_connector.mysql_connector_obj = self

    @staticmethod
    def get_instance():
        mysql_connector()
        logger.info("MySql Connection is established.")
        return mysql_connector.mysql_connector_obj

  
    