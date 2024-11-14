from litestar import Controller, get, post, status_codes
from litestar.contrib.pydantic import PydanticDTO
from litestar.di import Provide
from litestar.exceptions import HTTPException

from application.schemas.habit import HabitDTO, HabitReturnDTO
from application.services.habit import HabitService
from presentation.dependencies import habit_service


class HabitController(Controller):

    dependencies = {"service": Provide(habit_service)}

    @post(
        path="/",
        summary="Добавление новой полезной привычки",
        dto=PydanticDTO[HabitDTO],
        return_dto=PydanticDTO[HabitReturnDTO],
    )
    async def add_new_habit(
        self,
        data: HabitDTO,
        service: HabitService,
    ) -> HabitReturnDTO:
        if await service.get_habit(title=data.title):
            raise HTTPException(
                status_code=status_codes.HTTP_400_BAD_REQUEST,
                detail=f"Привычка <{data.title}> уже существует у пользователя",
            )
        resp = await service.add_habit(data)
        return HabitReturnDTO.model_validate(resp)
