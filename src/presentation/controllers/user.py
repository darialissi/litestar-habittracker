from litestar import Controller, get, post, status_codes
from litestar.contrib.pydantic import PydanticDTO
from litestar.di import Provide
from litestar.exceptions import HTTPException

from application.schemas.user import UserDTO, UserReturnDTO
from application.services.user import UserService
from presentation.dependencies import user_service


class UserController(Controller):

    dependencies = {"service": Provide(user_service)}

    @post(
        path="/register",
        summary="Регистрация нового пользователя",
        dto=PydanticDTO[UserDTO],
        return_dto=PydanticDTO[UserReturnDTO],
    )
    async def register_user(
        self,
        data: UserDTO,
        service: UserService,
    ) -> UserReturnDTO:
        if await service.get_user(username=data.username):
            raise HTTPException(
                status_code=status_codes.HTTP_400_BAD_REQUEST,
                detail=f"Пользователь <{data.username}> уже существует",
            )
        resp = await service.add_user(data)
        return UserReturnDTO.model_validate(resp)
