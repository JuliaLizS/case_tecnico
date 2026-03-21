import os
import sys
import sqlite3
import pytest


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

os.chdir(ROOT)

from database.database import create_table
from database.connect import create_connection
from models import CreateUserRequest
from services.user_service import user_service


@pytest.fixture(scope="session", autouse=True)
def init_db_schema():
    create_table()


def _ensure_user(name: str, email: str, description: str) -> int:
    try:
        return user_service.create_user(
            CreateUserRequest(name=name, email=email, description=description)
        )
    except Exception:
        conn = create_connection()
        row = conn.execute(
            "SELECT id FROM users WHERE email = ?",
            (email,),
        ).fetchone()
        conn.close()
        if row:
            return row[0]
        raise


@pytest.fixture(scope="session")
def seeded_users() -> dict[str, int]:
    return {
        "ana": _ensure_user(
            name="Ana Silva",
            email="ana.silva@example.com",
            description="Engenheira de software especializada em backend Python e APIs REST.",
        ),
        "carlos": _ensure_user(
            name="Carlos Mendes",
            email="carlos.mendes@example.com",
            description="Cientista de dados com foco em machine learning e análise de dados.",
        ),
        "beatriz": _ensure_user(
            name="Beatriz Costa",
            email="beatriz.costa@example.com",
            description="Desenvolvedora frontend com experiência em React e design de interfaces.",
        ),
        "seed_get_user": _ensure_user(
            name="Usuário Seed",
            email="seed.get_user@example.com",
            description="Usuário criado para teste de get_user.",
        ),
    }


@pytest.fixture(scope="session")
def seed_users(seeded_users):
    return seeded_users


@pytest.fixture()
def get_user_id_by_email():
    def _getter(email: str):
        conn = create_connection()
        row = conn.execute(
            "SELECT id FROM users WHERE email = ?",
            (email,),
        ).fetchone()
        conn.close()
        return row[0] if row else None

    return _getter
