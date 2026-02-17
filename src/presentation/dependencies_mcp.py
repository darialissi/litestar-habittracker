import os
from functools import wraps

from fastmcp import Context
from fastmcp.dependencies import CurrentContext, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from application.schemas.auth import TokenSchema, UserSchema
from application.services.auth import AuthService
from application.services.errors import TokenInvalidError
from application.services.habit import HabitService
from application.services.user import UserService
from config import settings
from domain.repositories.habit import HabitRepository
from domain.repositories.habit_dates import HabitDatesRepository
from domain.repositories.user import UserRepository
from infrastructure.database import sqlalchemy_config
from presentation.auth.errors import NotAuthorizedException


def with_db_session(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with sqlalchemy_config.get_session() as session:
            kwargs["db_session"] = session
            return await func(*args, **kwargs)

    return wrapper


def get_auth_service():
    return AuthService(
        secret_key=settings.TOKEN_KEY_SECRET,
        expired_minutes=settings.TOKEN_EXPIRE_MINUTES,
    )


@with_db_session
async def get_user_service(db_session: AsyncSession = None):
    return UserService(UserRepository(session=db_session))


@with_db_session
async def get_habit_service(db_session: AsyncSession = None):
    return HabitService(
        HabitRepository(session=db_session), HabitDatesRepository(session=db_session)
    )


async def get_auth_user(
    ctx: Context = CurrentContext(), auth_service: AuthService = Depends(get_auth_service)
) -> UserSchema:

    username = await ctx.get_state("auth_username")

    if username:
        return UserSchema(username=username)

    token = os.getenv("MCP_AUTH_TOKEN")  # токен клиента

    if not token:
        raise NotAuthorizedException(
            "You are unauthorized! Please set MCP_AUTH_TOKEN environment variable"
        )

    try:
        token_decoded: TokenSchema = auth_service.validate_token(token)
    except TokenInvalidError as exc:
        await ctx.debug(exc)
        raise NotAuthorizedException(f"You are unauthorized! Please set valid MCP_AUTH_TOKEN")

    user = UserSchema(username=token_decoded.sub)

    await ctx.set_state("auth_username", user.username)

    await ctx.debug(f"User {user.username} authenticated successfully")

    return user
