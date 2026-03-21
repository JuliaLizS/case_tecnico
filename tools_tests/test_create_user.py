# Testes da tool: create_user

from _helpers import init_db, section, ok, err

init_db()

from models import CreateUserRequest
from services.user_service import user_service


def run():
    section("TOOL 1 - create_user: criação válida")

    users_to_create = [
        CreateUserRequest(
            name="Ana Silva",
            email="ana.silva@example.com",
            description="Engenheira de software especializada em backend Python e APIs REST."
        ),
        CreateUserRequest(
            name="Carlos Mendes",
            email="carlos.mendes@example.com",
            description="Cientista de dados com foco em machine learning e análise de dados."
        ),
        CreateUserRequest(
            name="Beatriz Costa",
            email="beatriz.costa@example.com",
            description="Desenvolvedora frontend com experiência em React e design de interfaces."
        ),
    ]

    created_ids = []
    for user in users_to_create:
        try:
            user_id = user_service.create_user(user)
            created_ids.append(user_id)
            ok(f"Usuário '{user.name}' criado com ID: {user_id}")
        except Exception as e:
            if "UNIQUE constraint" in str(e):
                # Usuário já existe — busca o ID existente
                import sqlite3
                from database.connect import create_connection
                conn = create_connection()
                row = conn.execute(
                    "SELECT id FROM users WHERE email = ?", (user.email,)
                ).fetchone()
                conn.close()
                if row:
                    created_ids.append(row[0])
                    ok(f"Usuário '{user.name}' já existe com ID: {row[0]} (pulando criação)")
                else:
                    err(f"Falha ao criar '{user.name}': {e}")
            else:
                err(f"Falha ao criar '{user.name}': {e}")

    section("create_user: e-mail duplicado (deve falhar)")
    try:
        user_service.create_user(users_to_create[0])
        err("Deveria ter falhado, mas não falhou!")
    except Exception as e:
        ok(f"Erro esperado capturado: {e}")

    section("create_user: campos inválidos (e-mail malformado)")
    try:
        CreateUserRequest(name="Teste", email="email-invalido", description="desc")
        err("Deveria ter falhado na validação do e-mail!")
    except Exception as e:
        ok(f"Validação Pydantic funcionando: {e}")

    return created_ids


if __name__ == "__main__":
    ids = run()
    print(f"\n  IDs criados: {ids}")
    print(f"\n{'='*50}")
    print("  Testes de create_user concluídos.")
    print('='*50 + "\n")
