from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, ConfigDict


class UserCreate(BaseModel):
    """
    Данные для создания пользователя.
    """

    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """
    Данные пользователя, которые возвращаем наружу.
    """

    id: UUID
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class UserLogin(BaseModel):
    """
    Данные для входа.
    """

    email: EmailStr
    password: str