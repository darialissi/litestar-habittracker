from litestar import Controller, Request, Response, get, patch, post, status_codes
from litestar.contrib.pydantic import PydanticDTO
from litestar.datastructures import State
from litestar.di import Provide

from application.schemas.auth import TokenDecodedSchema, UserSchema
from application.schemas.habit import (
    ExtendedHabitReturnDTO,
    HabitCounterUpdateDTO,
    HabitDTO,
    HabitReturnDTO,
)
from application.schemas.responses import ResponseSchema
from application.services import errors
from application.services.habit import HabitService
from presentation.dependencies import get_habit_service


class HabitController(Controller):

    return_dto = PydanticDTO[ResponseSchema]

    dependencies = {"service": Provide(get_habit_service)}

    @post(
        path="/",
        summary="Добавление новой полезной привычки",
        dto=PydanticDTO[HabitDTO],
    )
    async def add_new_habit(
        self,
        data: HabitDTO,
        request: Request[UserSchema, TokenDecodedSchema, State],
        service: HabitService,
    ) -> Response[ResponseSchema]:

        response = ResponseSchema()

        try:
            resp = await service.add_new_habit(data=data, username=request.user.username)
        except errors.HabitAlreadyExistsError as exc:
            response.errors.append(exc.message)
            return Response(response, status_code=status_codes.HTTP_400_BAD_REQUEST)

        response.payload = HabitReturnDTO.model_validate(resp).model_dump()

        return Response(response)

    @patch(
        path="/",
        summary="Обновление полезной привычки по названию (счетчик +1)",
        dto=PydanticDTO[HabitCounterUpdateDTO],
    )
    async def update_habit(
        self,
        data: HabitCounterUpdateDTO,
        request: Request[UserSchema, TokenDecodedSchema, State],
        service: HabitService,
    ) -> Response[ResponseSchema]:

        response = ResponseSchema()

        try:
            habit = await service.update_habit(data=data, username=request.user.username)

        except errors.HabitNotFoundError as exc:
            response.errors.append(exc.message)
            return Response(response, status_code=status_codes.HTTP_404_NOT_FOUND)

        except errors.HabitAlreadyCompletedTodayError as exc:
            response.errors.append(exc.message)
            return Response(response, status_code=status_codes.HTTP_400_BAD_REQUEST)

        response.payload = HabitReturnDTO.model_validate(habit).model_dump()

        return Response(response)

    @get(
        path="/",
        summary="Получение всех полезных привычек пользователя",
    )
    async def get_user_habits(
        self,
        request: Request[UserSchema, TokenDecodedSchema, State],
        service: HabitService,
    ) -> Response[ResponseSchema]:

        response = ResponseSchema()

        if not (habits := await service.get_all_habits(author=request.user.username)):
            response.errors.append(
                f"У пользователя <{request.user.username}> еще нет полезных привычек"
            )
            return Response(response, status_code=status_codes.HTTP_404_NOT_FOUND)

        response.payload = {
            "habits": [HabitReturnDTO.model_validate(habit).model_dump() for habit in habits]
        }
        return Response(response)

    @get(
        path="/statistics",
        summary="Получение статистики выполнения заданной привычки за текущий период",
        description="Метод возвращает метрики выполнения заданной привычки в текущем периоде (скользящее окно) и общую статистику по привычке",
    )
    async def get_user_habit_statistics(
        self,
        title: str,
        request: Request[UserSchema, TokenDecodedSchema, State],
        service: HabitService,
    ) -> Response[ResponseSchema]:

        response = ResponseSchema()

        try:
            extended_habit = await service.get_current_period_extended_habit(
                title=title, author=request.user.username
            )
        except errors.HabitNotFoundError as exc:
            response.errors.append(exc.message)
            return Response(response, status_code=status_codes.HTTP_404_NOT_FOUND)

        model = ExtendedHabitReturnDTO.model_validate(extended_habit)

        response.payload = model.model_dump()
        return Response(response)

    @get(
        path="/overall",
        summary="Получение статистики выполнения всех привычек за заданный период",
        description="Метод возвращает метрики выполнения всех привычек пользователя в заданном периоде и общую статистику по привычкам",
    )
    async def get_user_habits_overall(
        self,
        days: int,
        request: Request[UserSchema, TokenDecodedSchema, State],
        service: HabitService,
    ) -> Response[ResponseSchema]:

        response = ResponseSchema()

        extended_habits = await service.get_defined_period_extended_habits(
            author=request.user.username, limit_days=days
        )

        response.payload["habits"] = [
            ExtendedHabitReturnDTO.model_validate(habit).model_dump() for habit in extended_habits
        ]

        return Response(response)
