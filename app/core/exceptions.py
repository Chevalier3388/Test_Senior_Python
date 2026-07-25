class UserAlreadyExistsError(Exception):
    def __init__(
        self,
        message: str = "Пользователь с таким адресом электронной почты уже существует",
    ) -> None:
        super().__init__(message)


class InvalidCredentialsError(Exception):
    def __init__(
        self,
        message: str = "Неверный email или пароль",
    ) -> None:
        super().__init__(message)
