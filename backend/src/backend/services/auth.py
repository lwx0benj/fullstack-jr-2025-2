from __future__ import annotations

import secrets
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional, Tuple

import jwt  # PyJWT
from pwdlib import PasswordHash

from backend.settings import Settings


_auth_singleton: Optional['Auth'] = None


def get_auth():
    global _auth_singleton
    if _auth_singleton is None:
        _auth_singleton = Auth()
    return _auth_singleton


class Auth:
    def __init__(self):
        self.settings = Settings()
        self._pwd = PasswordHash.recommended()
        self._revoked_jtis: set[str] = set()

    def hash_password(self, plain_password: str) -> str:
        return self._pwd.hash(plain_password)

    def verify_password(self, plain_password: str, password_hash: str) -> bool:
        try:
            return self._pwd.verify(plain_password, password_hash)
        except Exception:
            return False

    # -------- Token helpers --------
    def _encode(
        self,
        *,
        sub: str | int,
        ttl: timedelta,
        extra_claims: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Cria um token JWT assinado."""
        now = datetime.now(timezone.utc)
        jti = secrets.token_urlsafe(16)

        payload: Dict[str, Any] = {
            'iss': self.settings.JWT_ISSUER,
            'sub': str(sub),
            'iat': int(now.timestamp()),
            'nbf': int(now.timestamp()),
            'exp': int((now + ttl).timestamp()),
            'jti': jti,
            'token_use': 'access',
        }

        if getattr(self.settings, 'JWT_AUDIENCE', None):
            payload['aud'] = self.settings.JWT_AUDIENCE

        if extra_claims:
            payload.update(extra_claims)

        return jwt.encode(
            payload,
            self.settings.JWT_SECRET,
            algorithm=self.settings.JWT_ALGORITHM,
        )

    def _decode(self, token: str) -> Dict[str, Any]:
        options = {'require': ['exp', 'iat', 'nbf', 'iss', 'sub', 'jti']}

        kwargs: Dict[str, Any] = {
            'algorithms': [self.settings.JWT_ALGORITHM],
            'issuer': self.settings.JWT_ISSUER,
            'options': options,
        }

        if getattr(self.settings, 'JWT_AUDIENCE', None):
            kwargs['audience'] = self.settings.JWT_AUDIENCE

        payload = jwt.decode(token, self.settings.JWT_SECRET, **kwargs)

        if payload.get('token_use') != 'access':
            raise jwt.InvalidTokenError('Tipo de token inesperado.')
        if payload.get('jti') in self._revoked_jtis:
            raise jwt.InvalidTokenError('Token revogado.')

        return payload

    # -------- API --------
    def generate_token(
        self,
        *,
        subject: str | int,
        extra_claims: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        token = self._encode(
            sub=subject,
            ttl=timedelta(minutes=self.settings.JWT_TTL_MINUTES),
            extra_claims=extra_claims,
        )
        return {
            'access_token': token,
            'expires_in': self.settings.JWT_TTL_MINUTES * 60,
            'token_type': 'Bearer',
        }

    def verify_token(
        self, token: str
    ) -> Tuple[bool, Optional[Dict[str, Any]], Optional[str]]:
        try:
            payload = self._decode(token)
            return True, payload, None
        except jwt.ExpiredSignatureError:
            return False, None, 'expired'
        except jwt.InvalidTokenError as e:
            return False, None, f'invalid: {e}'

    def revoke_by_jti(self, jti: str) -> None:
        self._revoked_jtis.add(jti)

    def revoke_token(self, token: str) -> bool:
        try:
            options = {'verify_exp': False, 'require': ['iss', 'sub', 'jti']}
            kwargs: Dict[str, Any] = {
                'algorithms': [self.settings.JWT_ALGORITHM],
                'issuer': self.settings.JWT_ISSUER,
                'options': options,
            }

            if getattr(self.settings, 'JWT_AUDIENCE', None):
                kwargs['audience'] = self.settings.JWT_AUDIENCE

            payload = jwt.decode(token, self.settings.JWT_SECRET, **kwargs)
            jti = payload.get('jti')
            if jti:
                self._revoked_jtis.add(jti)
                return True
        except Exception:
            pass
        return False
