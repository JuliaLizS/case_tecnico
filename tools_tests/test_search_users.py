from models import SearchUserRequest
from services.user_service import user_service


def test_search_users_queries_semantic_top1(seed_users):
    queries = [
        ("Python backend desenvolvimento de APIs", "Ana Silva"),
        ("machine learning inteligência artificial", "Carlos Mendes"),
        ("React frontend interface web", "Beatriz Costa"),
    ]

    for query_text, expected_top in queries:
        results = user_service.search_users(SearchUserRequest(query=query_text, top_k=3))
        assert results
        assert results[0]["name"] == expected_top


def test_search_users_respects_top_k(seed_users):
    results = user_service.search_users(SearchUserRequest(query="desenvolvedor", top_k=1))
    assert len(results) <= 1


def test_search_users_empty_query_does_not_break(seed_users):
    results = user_service.search_users(SearchUserRequest(query="", top_k=3))
    assert isinstance(results, list)
