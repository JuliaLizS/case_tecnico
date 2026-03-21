# Utilitários e setup compartilhados entre os testes

import sys
import os
import logging

# Aponta para a raiz do projeto
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# Muda o CWD para a raiz do projeto (garante que o FAISS use caminho correto)
os.chdir(ROOT)

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")


def init_db():
    from database.database import create_table
    create_table()
    logging.info("*** Banco de dados inicializado. ***")


def section(title: str):
    print(f"\n{'='*50}")
    print(f"  {title}")
    print('='*50)


def ok(msg: str):
    print(f"  OK {msg}")


def err(msg: str):
    print(f"  ERRO: {msg}")
