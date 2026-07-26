from datetime import UTC, datetime, timedelta
from uuid import UUID

import jwt
from pwdlib import PasswordHash

from app.core.config import settings

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Возвращает хеш пароля."""
    return password_hash.hash(password)


def verify_password(password: str, password_hash_value: str) -> bool:
    """Проверяет соответствие пароля его хешу."""
    return password_hash.verify(password, password_hash_value)


def _create_token(
    user_id: UUID,
    expires_delta: timedelta,
    token_type: str,
) -> str:
    """Создает JWT-токен."""

    payload = {
        "sub": str(user_id),
        "type": token_type,
        "exp": datetime.now(UTC) + expires_delta,
    }

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


def create_access_token(user_id: UUID) -> str:
    """Создает access token."""

    return _create_token(
        user_id=user_id,
        expires_delta=timedelta(
            minutes=settings.access_token_expire_minutes,
        ),
        token_type="access",
    )


def decode_token(token: str) -> dict:
    """Декодирует JWT-токен."""

    return jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm],
    )
