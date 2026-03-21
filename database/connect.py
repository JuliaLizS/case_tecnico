# Conexão SQLite

import sqlite3
import os
import logging
from logging_config import configure_logging

configure_logging()
logger = logging.getLogger(__name__)

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'users.db')

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        logger.debug("Conexão SQLite estabelecida", extra={"event": "db_connect_success"})
    except sqlite3.Error as e:
        logger.error(
            "Erro ao conectar ao banco de dados",
            extra={"event": "db_connect_error", "error": str(e)}
        )
    return conn
