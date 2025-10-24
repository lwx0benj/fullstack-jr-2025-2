from http import HTTPStatus

from sqlalchemy import select

from backend.models.users import User
from backend.services.auth import Auth


# Register
def test_register_success_returns_token_and_persists_user(client, session):
    payload = {
        'name': 'Ada Lovelace',
        'email': 'ada@example.com',
        'password': 'S3nh@-muito-segura',
    }

    resp = client.post('/api/auth/register', json=payload)
    assert resp.status_code == HTTPStatus.CREATED

    data = resp.json()

    assert set(data.keys()) == {'access_token', 'token_type', 'expires_in'}
    assert isinstance(data['access_token'], str) and data['access_token']
    assert data['token_type'] == 'Bearer'
    assert isinstance(data['expires_in'], int) and data['expires_in'] > 0

    db_user = session.scalar(select(User).where(User.email == payload['email']))
    assert db_user is not None
    assert db_user.name == payload['name']
    assert db_user.email == payload['email']

    assert db_user.hashed_password != payload['password']

    auth = Auth()
    assert auth.verify_password(payload['password'], db_user.hashed_password) is True


def test_register_conflict_when_email_already_exists(client, session):
    existing = User(
        name='Ada',
        email='ada@example.com',
        hashed_password='qualquer-hash',
    )
    session.add(existing)
    session.commit()

    payload = {
        'name': 'Outra Pessoa',
        'email': 'ada@example.com',
        'password': 'abc123',
    }

    resp = client.post('/api/auth/register', json=payload)
    assert resp.status_code == HTTPStatus.CONFLICT

    body = resp.json()

    assert body.get('detail') == 'Usuário já cadastrado.'

    count = session.scalars(select(User).where(User.email == payload['email'])).all()
    assert len(count) == 1


# Login
def _create_user(
    session, *, name='Ada Lovelace', email='ada@example.com', password='S3nh@F0rte'
):
    auth = Auth()
    hashed = auth.hash_password(password)
    user = User(name=name, email=email, hashed_password=hashed)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def test_login_success_returns_token(client, session):
    user = _create_user(session)

    payload = {'email': user.email, 'password': 'S3nh@F0rte'}
    resp = client.post('/api/auth/login', json=payload)

    assert resp.status_code == HTTPStatus.OK
    data = resp.json()
    assert set(data.keys()) == {'access_token', 'token_type', 'expires_in'}
    assert data['token_type'] == 'Bearer'
    assert isinstance(data['access_token'], str) and data['access_token']
    assert isinstance(data['expires_in'], int) and data['expires_in'] > 0

    auth = Auth()
    ok, payload_out, err = auth.verify_token(data['access_token'])
    assert ok is True, err
    assert payload_out['sub'] == str(user.id)
    assert payload_out['email'] == user.email
    assert payload_out['name'] == user.name
    assert payload_out['token_use'] == 'access'


def test_login_invalid_email_returns_401(client):
    payload = {'email': 'naoexiste@example.com', 'password': 'qualquer'}
    resp = client.post('/api/auth/login', json=payload)

    assert resp.status_code == HTTPStatus.UNAUTHORIZED
    body = resp.json()
    assert body.get('detail') == 'Credenciais inválidas.'


def test_login_wrong_password_returns_401(client, session):
    user = _create_user(session, password='senha-correta')

    payload = {'email': user.email, 'password': 'senha-errada'}
    resp = client.post('/api/auth/login', json=payload)

    assert resp.status_code == HTTPStatus.UNAUTHORIZED
    body = resp.json()
    assert body.get('detail') == 'Credenciais inválidas.'


# Userinfo
def test_userinfo_success_returns_user_info(client, session):
    user = _create_user(session)
    login_payload = {'email': user.email, 'password': 'S3nh@F0rte'}
    login_resp = client.post('/api/auth/login', json=login_payload)
    assert login_resp.status_code == HTTPStatus.OK
    token = login_resp.json()['access_token']

    # Act
    resp = client.get(
        '/api/auth/userinfo',
        headers={'Authorization': f'Bearer {token}'},
    )

    # Assert
    assert resp.status_code == HTTPStatus.OK
    data = resp.json()
    assert set(data.keys()) == {'id', 'name', 'email'}
    assert data['id'] == user.id
    assert data['name'] == user.name
    assert data['email'] == user.email


def test_userinfo_missing_token_returns_401(client):
    resp = client.get('/api/auth/userinfo')
    assert resp.status_code == HTTPStatus.UNAUTHORIZED
    body = resp.json()
    assert (
        body.get('detail')
        == 'Token ausente ou esquema inválido. Use Authorization: Bearer <token>.'
    )


def test_userinfo_wrong_scheme_returns_401(client):
    resp = client.get(
        '/api/auth/userinfo',
        headers={'Authorization': 'Basic abc.def.ghi'},
    )
    assert resp.status_code == HTTPStatus.UNAUTHORIZED
    body = resp.json()
    assert (
        body.get('detail')
        == 'Token ausente ou esquema inválido. Use Authorization: Bearer <token>.'
    )


def test_userinfo_invalid_token_returns_401(client):
    resp = client.get(
        '/api/auth/userinfo',
        headers={'Authorization': 'Bearer invalido.token.aqui'},
    )
    assert resp.status_code == HTTPStatus.UNAUTHORIZED
    body = resp.json()
    assert body.get('detail') == 'Token inválido ou expirado.'


def test_userinfo_token_without_sub_returns_401(client, monkeypatch):
    def fake_verify_token(_self, _token: str):
        return True, {'email': 'x@y.com'}, None

    monkeypatch.setattr(Auth, 'verify_token', fake_verify_token)

    resp = client.get(
        '/api/auth/userinfo',
        headers={'Authorization': 'Bearer qualquer.coisa'},
    )
    assert resp.status_code == HTTPStatus.UNAUTHORIZED
    body = resp.json()
    assert body.get('detail') == 'Token inválido ou expirado.'


def test_userinfo_user_not_found_returns_404(client, monkeypatch, session):
    not_exists = session.get(User, 999999)
    assert not_exists is None

    def fake_verify_token(_self, _token: str):
        # ok, payload, err
        return True, {'sub': '999999'}, None

    monkeypatch.setattr(Auth, 'verify_token', fake_verify_token)

    resp = client.get(
        '/api/auth/userinfo',
        headers={'Authorization': 'Bearer token-valido-mas-user-nao-existe'},
    )
    assert resp.status_code == HTTPStatus.NOT_FOUND
    body = resp.json()
    assert body.get('detail') == 'Usuário não encontrado.'


# Logout
def test_logout_success_revokes_token_and_returns_204(client, session):
    user = _create_user(session)
    login_payload = {'email': user.email, 'password': 'S3nh@F0rte'}
    login_resp = client.post('/api/auth/login', json=login_payload)
    assert login_resp.status_code == HTTPStatus.OK
    token = login_resp.json()['access_token']

    resp = client.post(
        '/api/auth/logout',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert resp.status_code == HTTPStatus.NO_CONTENT

    userinfo_resp = client.get(
        '/api/auth/userinfo',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert userinfo_resp.status_code == HTTPStatus.UNAUTHORIZED
    assert userinfo_resp.json().get('detail') == 'Token inválido ou expirado.'


def test_logout_is_idempotent(client, session):
    user = _create_user(session, email='ada2@example.com')
    login_payload = {'email': user.email, 'password': 'S3nh@F0rte'}
    login_resp = client.post('/api/auth/login', json=login_payload)
    assert login_resp.status_code == HTTPStatus.OK
    token = login_resp.json()['access_token']

    resp1 = client.post(
        '/api/auth/logout',
        headers={'Authorization': f'Bearer {token}'},
    )

    resp2 = client.post(
        '/api/auth/logout',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert resp1.status_code == HTTPStatus.NO_CONTENT
    assert resp2.status_code == HTTPStatus.NO_CONTENT

    userinfo_resp = client.get(
        '/api/auth/userinfo',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert userinfo_resp.status_code == HTTPStatus.UNAUTHORIZED
    assert userinfo_resp.json().get('detail') == 'Token inválido ou expirado.'


def test_logout_without_authorization_header_returns_204(client):
    resp = client.post('/api/auth/logout')

    assert resp.status_code == HTTPStatus.NO_CONTENT


def test_logout_with_wrong_scheme_returns_204(client, session):
    _create_user(session, email='ada3@example.com')
    resp = client.post(
        '/api/auth/logout',
        headers={'Authorization': 'Basic abc.def.ghi'},
    )

    assert resp.status_code == HTTPStatus.NO_CONTENT
