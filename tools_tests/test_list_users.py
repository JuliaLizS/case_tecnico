from models import ListUsersRequest
from services.user_service import user_service


def test_list_users_basic_listing(seed_users):
    result = user_service.list_users(ListUsersRequest(limit=10, offset=0))
    assert isinstance(result, list)
    assert len(result) > 0
    assert all("id" in user and "name" in user and "email" in user for user in result)


def test_list_users_respects_limit(seed_users):
    result = user_service.list_users(ListUsersRequest(limit=2, offset=0))
    assert len(result) <= 2


def test_list_users_pagination_by_offset(seed_users):
    page1 = user_service.list_users(ListUsersRequest(limit=2, offset=0))
    page2 = user_service.list_users(ListUsersRequest(limit=2, offset=2))

    ids_p1 = {user["id"] for user in page1}
    ids_p2 = {user["id"] for user in page2}
    assert ids_p1.isdisjoint(ids_p2)


def test_list_users_offset_out_of_range_returns_empty(seed_users):
    result = user_service.list_users(ListUsersRequest(limit=10, offset=99999))
    assert result == []
