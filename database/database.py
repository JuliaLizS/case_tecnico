# criação da tabela de usuários
import sqlite3
from connect import create_connection


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
            print("Tabela de usuários criada com sucesso!")
        except sqlite3.Error as e:
            print(f"Erro ao criar a tabela: {e}")
        finally:
            conn.close()
    else:
        print("Erro! Não foi possível estabelecer a conexão com o banco de dados.")

def create_user(name, email, description):
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (name, email, description)
                VALUES (?, ?, ?)
            ''', (name, email, description))
            conn.commit()
            print("Usuário criado com sucesso!")
        except sqlite3.Error as e:
            print(f"Erro ao criar o usuário: {e}")
        finally:
            conn.close()
    else:
        print("Erro! Não foi possível estabelecer a conexão com o banco de dados.")