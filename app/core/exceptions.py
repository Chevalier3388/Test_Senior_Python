class UserAlreadyExistsError(Exception):
    """Пользователь с таким email уже существует."""


class InvalidCredentialsError(Exception):
    """Неверный email или пароль."""
