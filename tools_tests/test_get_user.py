from services.user_service import user_service


def test_get_user_id_existent(seeded_users):
    user_id = seeded_users["seed_get_user"]
    user = user_service.get_user(user_id)

    assert user is not None
    assert user.id == user_id
    assert user.email == "seed.get_user@example.com"


def test_get_user_id_nonexistent_returns_none():
    user = user_service.get_user(9999)
    assert user is None


def test_get_user_id_negative_returns_none():
    user = user_service.get_user(-1)
    assert user is None
