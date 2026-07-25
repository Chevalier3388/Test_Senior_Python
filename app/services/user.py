from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import UserAlreadyExistsError, InvalidCredentialsError
from app.core.security import hash_password, verify_password
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserLogin


class UserService:
    """Сервис работы с пользователями."""

    def __init__(
        self,
        session: AsyncSession,
    ):
        self.repository = UserRepository(session)

    async def create_user(
        self,
        data: UserCreate,
    ) -> User:
        """Создает нового пользователя."""

        existing_user = await self.repository.get_by_email(data.email)

        if existing_user:
            raise UserAlreadyExistsError(
                "Пользователь с таким адресом электронной почты уже существует"
            )

        user = User(
            email=data.email,
            password_hash=hash_password(data.password),
        )

        return await self.repository.create(user)

    async def get_user(
        self,
        user_id: UUID,
    ) -> User | None:
        """Возвращает пользователя по ID."""

        return await self.repository.get_by_id(user_id)

    async def authenticate(
            self,
            data: UserLogin,
    ) -> User:
        """Проверяет пользователя и пароль."""

        user = await self.repository.get_by_email(
            data.email
        )

        if not user:
            raise InvalidCredentialsError(
                "Неверный email или пароль"
            )

        if not verify_password(
                data.password,
                user.password_hash,
        ):
            raise InvalidCredentialsError(
                "Неверный email или пароль"
            )

        return user
