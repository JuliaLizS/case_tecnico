# Testes da tool: list_users

from _helpers import init_db, section, ok, err

init_db()

from models import CreateUserRequest, ListUsersRequest
from services.user_service import user_service

SEED_USERS = [
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


def seed_users():
    for user in SEED_USERS:
        try:
            user_service.create_user(user)
        except Exception:
            pass  # já existe


def run():
    seed_users()

    section("TOOL 4 - list_users: listagem básica")
    try:
        result = user_service.list_users(ListUsersRequest(limit=10, offset=0))
        if result:
            ok(f"Retornou {len(result)} usuário(s).")
            for u in result:
                ok(f"  [{u['id']}] {u['name']} | {u['email']}")
        else:
            err("Nenhum usuário retornado.")
    except Exception as e:
        err(f"Erro inesperado: {e}")

    section("list_users: paginação com limit=2 offset=0")
    try:
        result = user_service.list_users(ListUsersRequest(limit=2, offset=0))
        if len(result) <= 2:
            ok(f"limit=2 respeitado: {len(result)} resultado(s).")
        else:
            err(f"limit=2 não respeitado: {len(result)} resultados.")
    except Exception as e:
        err(f"Erro inesperado: {e}")

    section("list_users: paginação com limit=2 offset=2")
    try:
        page1 = user_service.list_users(ListUsersRequest(limit=2, offset=0))
        page2 = user_service.list_users(ListUsersRequest(limit=2, offset=2))
        ids_p1 = {u["id"] for u in page1}
        ids_p2 = {u["id"] for u in page2}
        if ids_p1.isdisjoint(ids_p2):
            ok("Páginas não se sobrepõem — offset funcionando corretamente.")
        else:
            err(f"IDs repetidos entre páginas: {ids_p1 & ids_p2}")
    except Exception as e:
        err(f"Erro inesperado: {e}")

    section("list_users: offset além do total (deve retornar lista vazia)")
    try:
        result = user_service.list_users(ListUsersRequest(limit=10, offset=99999))
        if result == []:
            ok("Retornou lista vazia para offset fora do range.")
        else:
            err(f"Deveria ser [], mas retornou: {result}")
    except Exception as e:
        err(f"Erro inesperado: {e}")


if __name__ == "__main__":
    run()
    print(f"\n{'='*50}")
    print("  Testes de list_users concluídos.")
    print('='*50 + "\n")
