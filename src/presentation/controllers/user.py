from datetime import timedelta

from litestar import Controller, Request, Response, get, post
from litestar.contrib.pydantic import PydanticDTO
from litestar.datastructures import Cookie, State
from litestar.di import Provide

from application.schemas.auth import AuthSchema, TokenSchema, UserSchema
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

        user = await service.add_or_get_user(data)

        auth_result: AuthSchema = auth_service.create_token(username=data.username)

        resp = Response(
            UserReturnDTO.model_validate(user),
            cookies=[
                Cookie(
                    key=settings.AUTH_COOKIE,
                    value=auth_result.token,
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
