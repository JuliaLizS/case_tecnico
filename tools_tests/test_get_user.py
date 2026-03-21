# Testes da tool: get_user

from _helpers import init_db, section, ok, err
from models import CreateUserRequest
from services.user_service import user_service
#import sqlite3

init_db()

def seed_user() -> int:
    """Garante que existe ao menos um usuário para buscar."""
    try:
        user_id = user_service.create_user(CreateUserRequest(
            name="Usuário Seed",
            email="seed.get_user@example.com",
            description="Usuário criado para teste de get_user."
        ))
        return user_id
    except Exception:
        # Usuário já existe, busca pelo e-mail no banco
        from database.connect import create_connection
        conn = create_connection()
        row = conn.execute(
            "SELECT id FROM users WHERE email = ?",
            ("seed.get_user@example.com",)
        ).fetchone()
        conn.close()
        return row[0] if row else None


def run():
    user_id = seed_user()

    section("TOOL 2 - get_user: ID existente")
    try:
        user = user_service.get_user(user_id)
        if user:
            ok(f"ID {user_id} → {user.name} | {user.email}")
        else:
            err(f"Usuário com ID {user_id} não encontrado.")
    except Exception as e:
        err(f"Erro inesperado ao buscar ID {user_id}: {e}")

    section("get_user: ID inexistente (deve retornar None)")
    try:
        user = user_service.get_user(9999)
        if user is None:
            ok("Retornou None corretamente para ID inexistente.")
        else:
            err(f"Deveria ser None, mas retornou: {user}")
    except Exception as e:
        err(f"Erro inesperado: {e}")

    section("get_user: ID negativo (deve retornar None)")
    try:
        user = user_service.get_user(-1)
        if user is None:
            ok("Retornou None corretamente para ID negativo.")
        else:
            err(f"Deveria ser None, mas retornou: {user}")
    except Exception as e:
        err(f"Erro inesperado: {e}")


if __name__ == "__main__":
    run()
    print("*** Testes de get_user concluídos. ***")
