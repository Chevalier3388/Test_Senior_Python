from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    InvalidCredentialsError,
    UserAlreadyExistsError,
)


async def user_already_exists_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """
    Обрабатывает ошибку существующего пользователя.
    """

    return JSONResponse(
        status_code=400,
        content={
            "detail": str(exc),
        },
    )


async def invalid_credentials_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """
    Обрабатывает ошибку авторизации.
    """

    return JSONResponse(
        status_code=401,
        content={
            "detail": str(exc),
        },
    )