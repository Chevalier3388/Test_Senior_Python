from fastapi import APIRouter, Depends, Query
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


@router.get(
    "",
    response_model=list[UserResponse],
)
async def get_users(
    limit: int = Query(
        default=50,
        ge=1,
        le=100,
    ),
    offset: int = Query(
        default=0,
        ge=0,
    ),
    session: AsyncSession = Depends(get_async_session),
) -> list[UserResponse]:
    """Возвращает список пользователей."""

    service = UserService(session)

    users = await service.get_users(
        limit=limit,
        offset=offset,
    )

    return [UserResponse.model_validate(user) for user in users]
