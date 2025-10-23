# tests/test_register_route.py
from http import HTTPStatus

from sqlalchemy import select

from backend.models.users import User
from backend.services.auth import Auth


def test_register_success_returns_token_and_persists_user(client, session):
    payload = {
        "name": "Ada Lovelace",
        "email": "ada@example.com",
        "password": "S3nh@-muito-segura",
    }

    resp = client.post("/api/auth/register", json=payload)
    assert resp.status_code == HTTPStatus.CREATED

    data = resp.json()
    
    assert set(data.keys()) == {"access_token", "token_type", "expires_in"}
    assert isinstance(data["access_token"], str) and data["access_token"]
    assert data["token_type"] == "Bearer"
    assert isinstance(data["expires_in"], int) and data["expires_in"] > 0

    db_user = session.scalar(select(User).where(User.email == payload["email"]))
    assert db_user is not None
    assert db_user.name == payload["name"]
    assert db_user.email == payload["email"]

    assert db_user.hashed_password != payload["password"]

    auth = Auth()
    assert auth.verify_password(payload["password"], db_user.hashed_password) is True


def test_register_conflict_when_email_already_exists(client, session):
    existing = User(
        name="Ada",
        email="ada@example.com",
        hashed_password="qualquer-hash",
    )
    session.add(existing)
    session.commit()

    payload = {
        "name": "Outra Pessoa",
        "email": "ada@example.com",
        "password": "abc123",
    }

    resp = client.post("/api/auth/register", json=payload)
    assert resp.status_code == HTTPStatus.CONFLICT

    body = resp.json()

    assert body.get("detail") == "Usuário já cadastrado."

    count = session.scalars(select(User).where(User.email == payload["email"])).all()
    assert len(count) == 1
