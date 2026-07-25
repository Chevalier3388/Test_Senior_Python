from typing import cast

from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import UserAlreadyExistsError


async def user_already_exists_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """
    Обрабатывает ошибку существующего пользователя.
    """
    error = cast(UserAlreadyExistsError, exc)

    return JSONResponse(
        status_code=400,
        content={
            "detail": str(error),
        },
    )
