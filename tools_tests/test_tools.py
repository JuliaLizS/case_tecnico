"""
Executar todos os testes das tools em sequência

Para rodar individualmente:
    python test_create_user.py
    python test_get_user.py
    python test_search_users.py
    python test_list_users.py
"""
import sys
import os
import test_create_user
import test_get_user
import test_search_users
import test_list_users

# Garante que _helpers e os módulos do projeto sejam encontrados
TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(TESTS_DIR)
if TESTS_DIR not in sys.path:
    sys.path.insert(0, TESTS_DIR)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


if __name__ == "__main__":
    test_create_user.run()
    test_get_user.run()
    test_search_users.run()
    test_list_users.run()

    print("*** Todos os testes concluídos. ***")

