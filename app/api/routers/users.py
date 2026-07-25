from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token
from app.db.database import get_async_session
from app.schemas.user import UserCreate, UserResponse, UserLogin, TokenResponse
from app.services.user import UserService


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201,
)
async def register(
    data: UserCreate,
    session: AsyncSession = Depends(get_async_session),
) -> UserResponse:
    """Регистрирует нового пользователя."""

    service = UserService(session)

    user = await service.create_user(data)

    return UserResponse.model_validate(user)


@router.post(
    "/login",
    response_model=TokenResponse,
)
async def login(
    data: UserLogin,
    session: AsyncSession = Depends(get_async_session),
) -> TokenResponse:
    """Авторизация пользователя."""

    service = UserService(session)

    user = await service.authenticate(data)

    token = create_access_token(user.id)

    return TokenResponse(
        access_token=token,
    )