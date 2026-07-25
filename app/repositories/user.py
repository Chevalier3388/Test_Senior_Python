from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserRepository:
    """Работа с пользователями в базе данных."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_email(self, email: str) -> User | None:
        """Получить пользователя по email."""

        result = await self.session.execute(select(User).where(User.email == email))

        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: UUID) -> User | None:
        """Получить пользователя по ID."""

        result = await self.session.execute(select(User).where(User.id == user_id))

        return result.scalar_one_or_none()

    async def create(
        self,
        user: User,
    ) -> User:
        """Создать пользователя."""

        self.session.add(user)

        await self.session.flush()

        return user
