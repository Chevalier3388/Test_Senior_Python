from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_async_session
from app.schemas.user import UserCreate, UserResponse
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