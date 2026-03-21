# Testes da tool: search_users

from _helpers import init_db, section, ok, err
from models import CreateUserRequest, SearchUserRequest
from services.user_service import user_service

init_db()

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
    """Garante que os usuários de referência existem no banco."""
    for user in SEED_USERS:
        try:
            user_service.create_user(user)
        except Exception:
            pass  # já existe


def run():
    seed_users()

    section("TOOL 3 - search_users: queries semânticas")

    queries = [
        ("Python backend desenvolvimento de APIs", "Ana Silva"),
        ("machine learning inteligência artificial", "Carlos Mendes"),
        ("React frontend interface web", "Beatriz Costa"),
    ]

    for query_text, expected_top in queries:
        req = SearchUserRequest(query=query_text, top_k=3)
        print(f"\n  Query: \"{query_text}\"")
        try:
            results = user_service.search_users(req)
            if results:
                top_result = results[0]
                for r in results:
                    ok(f"[score={r['score']:.4f}] {r['name']} — {r['description'][:55]}...")
                if top_result["name"] == expected_top:
                    ok(f"Resultado mais relevante correto: '{top_result['name']}'")
                else:
                    err(f"Esperado '{expected_top}', obtido '{top_result['name']}'")
            else:
                err("Nenhum resultado retornado.")
        except Exception as e:
            err(f"Erro na busca: {e}")

    section("search_users: top_k menor que total de usuários")
    try:
        req = SearchUserRequest(query="desenvolvedor", top_k=1)
        results = user_service.search_users(req)
        if len(results) <= 1:
            ok(f"top_k=1 respeitado: {len(results)} resultado(s).")
        else:
            err(f"top_k=1 não foi respeitado: {len(results)} resultados.")
    except Exception as e:
        err(f"Erro inesperado: {e}")

    section("search_users: query vazia")
    try:
        req = SearchUserRequest(query="", top_k=3)
        results = user_service.search_users(req)
        ok(f"Query vazia retornou {len(results)} resultado(s) sem crash.")
    except Exception as e:
        err(f"Erro inesperado com query vazia: {e}")


if __name__ == "__main__":
    run()
    print("*** Teste search_users concluídos. ***")
