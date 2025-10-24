import time
from datetime import datetime, timedelta, timezone

import jwt
import pytest

import backend.services.auth as auth_module
from backend.services.auth import Auth


@pytest.fixture
def patched_settings(monkeypatch):
    class TestSettings:
        JWT_ISSUER = 'test-issuer'
        JWT_AUDIENCE = None
        JWT_ALGORITHM = 'HS256'
        JWT_SECRET = 'test-secret'
        JWT_TTL_MINUTES = 1

    def func_settings():
        return TestSettings()

    monkeypatch.setattr(auth_module, 'Settings', func_settings)
    return TestSettings


@pytest.fixture
def auth(patched_settings):
    return Auth()


def test_hash_and_verify_password_success(auth):
    hashed = auth.hash_password('senha-forte')
    assert hashed
    assert isinstance(hashed, str)
    assert auth.verify_password('senha-forte', hashed) is True


def test_hash_and_verify_password_failure(auth):
    hashed = auth.hash_password('original')
    assert auth.verify_password('errada', hashed) is False


def test_generate_token_and_verify(auth, patched_settings):
    issued = auth.generate_token(subject='user-123', extra_claims={'role': 'admin'})
    assert 'access_token' in issued
    assert issued['token_type'] == 'Bearer'
    assert issued['expires_in'] == patched_settings.JWT_TTL_MINUTES * 60

    ok, payload, err = auth.verify_token(issued['access_token'])
    assert ok is True
    assert err is None
    assert payload['sub'] == 'user-123'
    assert payload['iss'] == patched_settings.JWT_ISSUER
    assert payload['token_use'] == 'access'
    assert payload['role'] == 'admin'  # extra_claims propagou


def test_expired_token_returns_expired(auth):
    token = auth._encode(sub='u1', ttl=timedelta(seconds=1))
    time.sleep(2)
    ok, payload, err = auth.verify_token(token)
    assert ok is False
    assert payload is None
    assert err == 'expired'


def test_revoke_by_jti_blocks_token(auth):
    token = auth._encode(sub='u1', ttl=timedelta(minutes=5))

    payload = auth._decode(token)
    jti = payload['jti']

    auth.revoke_by_jti(jti)
    ok, payload2, err = auth.verify_token(token)
    assert ok is False
    assert payload2 is None
    assert 'revogado' in err


def test_revoke_token_helper(auth):
    token = auth._encode(sub='u1', ttl=timedelta(minutes=5))
    assert auth.revoke_token(token) is True

    ok, payload, err = auth.verify_token(token)
    assert ok is False
    assert payload is None
    assert 'revogado' in err


def test_audience_happy_and_unhappy_paths(auth, patched_settings):
    auth.settings.JWT_AUDIENCE = 'web-client'
    token = auth._encode(sub='u1', ttl=timedelta(minutes=5))

    ok, payload, err = auth.verify_token(token)
    assert ok is True
    assert payload['aud'] == 'web-client'
    assert err is None

    auth.settings.JWT_AUDIENCE = 'another-client'
    ok2, payload2, err2 = auth.verify_token(token)
    assert ok2 is False
    assert payload2 is None
    assert err2.startswith('invalid:')


def test_invalid_token_use_returns_invalid(auth, patched_settings):
    now = datetime.now(timezone.utc)
    payload = {
        'iss': patched_settings.JWT_ISSUER,
        'sub': 'u1',
        'iat': int(now.timestamp()),
        'nbf': int(now.timestamp()),
        'exp': int((now + timedelta(minutes=5)).timestamp()),
        'jti': 'any-jti',
        'token_use': 'refresh',
    }
    token = jwt.encode(
        payload,
        patched_settings.JWT_SECRET,
        algorithm=patched_settings.JWT_ALGORITHM,
    )

    ok, payload_out, err = auth.verify_token(token)
    assert ok is False
    assert payload_out is None
    assert 'Tipo de token inesperado' in err


def test_generate_token_return_shape(auth, patched_settings):
    result = auth.generate_token(subject=42)
    assert set(result.keys()) == {'access_token', 'expires_in', 'token_type'}
    assert isinstance(result['access_token'], str)
    assert result['token_type'] == 'Bearer'
    assert result['expires_in'] == patched_settings.JWT_TTL_MINUTES * 60
