# Conexão SQLite

import sqlite3

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('users.db')
        print("Conexão estabelecida com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
    return conn
