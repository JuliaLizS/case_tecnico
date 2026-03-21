import sqlite3
import pytest
from pydantic import ValidationError

from models import CreateUserRequest
from services.user_service import user_service


def test_create_user_valid_creation(seeded_users):
    assert seeded_users["ana"] is not None
    assert seeded_users["carlos"] is not None
    assert seeded_users["beatriz"] is not None


def test_create_user_email_duplicate_raises_error(seeded_users):
    payload = CreateUserRequest(
        name="Ana Silva",
        email="ana.silva@example.com",
        description="Engenheira de software especializada em backend Python e APIs REST.",
    )

    with pytest.raises(sqlite3.Error):
        user_service.create_user(payload)


def test_create_user_email_invalid_raises_error():
    with pytest.raises(ValidationError):
        CreateUserRequest(name="Teste", email="email-invalido", description="desc")
