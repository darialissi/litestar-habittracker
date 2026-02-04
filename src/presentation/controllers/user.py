from datetime import timedelta

from litestar import Controller, Request, Response, get, post
from litestar.contrib.pydantic import PydanticDTO
from litestar.datastructures import Cookie, State
from litestar.di import Provide

from application.schemas.user import UserDTO, UserReturnDTO
from application.services.user import UserService
from config import settings
from presentation.auth.schemas import TokenSchema, UsernameSchema
from presentation.dependencies import user_service


class UserController(Controller):
    return_dto = PydanticDTO[UserReturnDTO]

    dependencies = {"service": Provide(user_service)}

    @post(
        path="/signin",
        summary="Аутентификация пользователя",
        dto=PydanticDTO[UserDTO],
    )
    async def auth_user(
        self,
        data: UserDTO,
        service: UserService,
    ) -> Response[UserReturnDTO]:

        user, token = await service.auth_user(data)

        resp = Response(
            UserReturnDTO.model_validate(user),
            cookies=[
                Cookie(
                    key=settings.AUTH_COOKIE,
                    value=token,
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
        request: Request[UsernameSchema, TokenSchema, State],
        service: UserService,
    ) -> Response[UserReturnDTO]:
        resp = await service.get_user(username=request.user.username)
        return Response(UserReturnDTO.model_validate(resp))
