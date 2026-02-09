from datetime import timedelta

from litestar import Controller, Request, Response, get, post, status_codes
from litestar.contrib.pydantic import PydanticDTO
from litestar.datastructures import Cookie, State
from litestar.di import Provide
from litestar.exceptions import HTTPException

from application.schemas.auth import (
    AuthSchema,
    TokenSchema,
    UserCred,
    UserCredMasked,
    UserSchema,
)
from application.schemas.user import UserDTO, UserReturnDTO
from application.services.auth import AuthService
from application.services.user import UserService
from config import settings
from presentation.dependencies import auth_service, user_service


class UserController(Controller):
    return_dto = PydanticDTO[UserReturnDTO]

    dependencies = {"service": Provide(user_service), "auth_service": Provide(auth_service)}

    @post(
        path="/signin",
        summary="Аутентификация пользователя",
        dto=PydanticDTO[UserDTO],
    )
    async def auth_user(
        self,
        data: UserDTO,
        service: UserService,
        auth_service: AuthService,
    ) -> Response[UserReturnDTO]:

        hashed_password = auth_service.hash_password(password=data.password)

        cred_masked = UserCredMasked(username=data.username, hashed_password=hashed_password)

        user = await service.add_or_get_user(cred_masked)

        cred = UserCred(
            username=data.username, password=data.password, hashed_password=user.hashed_password
        )

        auth_user: AuthSchema | None = auth_service.auth_user(cred)

        if not auth_user:
            raise HTTPException(
                status_code=status_codes.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        resp = Response(
            UserReturnDTO.model_validate(user),
            cookies=[
                Cookie(
                    key=settings.AUTH_COOKIE,
                    value=auth_user.token,
                    max_age=timedelta(minutes=settings.TOKEN_EXPIRE_MINUTES),
                    httponly=True,
                )
            ],
        )

        return resp

    @get(
        path="/me",
        summary="Получение данных активного пользователя",
    )
    async def get_auth_user(
        self,
        request: Request[UserSchema, TokenSchema, State],
        service: UserService,
    ) -> Response[UserReturnDTO]:
        resp = await service.get_user(username=request.user.username)
        return Response(UserReturnDTO.model_validate(resp))
