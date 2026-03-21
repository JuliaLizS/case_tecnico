# criação da tabela de usuários
import sqlite3
import logging
from database.connect import create_connection
from logging_config import configure_logging

configure_logging()
logger = logging.getLogger(__name__)


def create_table():
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    description TEXT
                )
            ''')
            conn.commit()
            logger.info("Tabela users verificada/criada", extra={"event": "users_table_ready"})
        except sqlite3.Error as e:
            logger.error("Erro ao criar a tabela users", extra={"event": "users_table_error", "error": str(e)})
        finally:
            conn.close()
    else:
        logger.error(
            "Não foi possível estabelecer conexão para criar a tabela",
            extra={"event": "users_table_connection_error"}
        )