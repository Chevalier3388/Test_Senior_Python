from fastapi import FastAPI

from app.api.routers.users import router as users_router
from app.core.exception_handlers import user_already_exists_handler
from app.core.exceptions import UserAlreadyExistsError

app = FastAPI(
    title="User API",
)

app.add_exception_handler(
    UserAlreadyExistsError,
    user_already_exists_handler,
)

app.include_router(users_router)
