from litestar import Controller, Request, Response, get, patch, post, status_codes
from litestar.contrib.pydantic import PydanticDTO
from litestar.datastructures import State
from litestar.di import Provide
from litestar.exceptions import HTTPException

from application.schemas.habit import (
    HabitCounterUpdateDTO,
    HabitDTO,
    HabitReturnDTO,
    HabitStatisticsReturn,
)
from application.services import errors
from application.services.habit import HabitService
from presentation.auth.schemas import TokenSchema, UsernameSchema
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
        request: Request[UsernameSchema, TokenSchema, State],
        service: HabitService,
    ) -> Response[HabitReturnDTO]:

        try:
            resp = await service.add_new_habit(data=data, username=request.user.username)
        except errors.HabitAlreadyExistsError as exc:
            raise HTTPException(
                status_code=status_codes.HTTP_400_BAD_REQUEST,
                detail=exc.message,
            )

        return Response(HabitReturnDTO.model_validate(resp))

    @patch(
        path="/",
        summary="Обновление полезной привычки по названию (счетчик +1)",
        dto=PydanticDTO[HabitCounterUpdateDTO],
        return_dto=PydanticDTO[HabitReturnDTO],
    )
    async def update_habit(
        self,
        data: HabitCounterUpdateDTO,
        request: Request[UsernameSchema, TokenSchema, State],
        service: HabitService,
    ) -> Response[HabitReturnDTO]:

        try:
            resp = await service.update_habit(data=data, username=request.user.username)
        except errors.HabitNotFoundError as exc:
            raise HTTPException(
                status_code=status_codes.HTTP_404_NOT_FOUND,
                detail=exc.message,
            )
        except errors.HabitAlreadyCompletedTodayError as exc:
            raise HTTPException(
                status_code=status_codes.HTTP_400_BAD_REQUEST,
                detail=exc.message,
            )

        return Response(HabitReturnDTO.model_validate(resp))

    @get(
        path="/",
        summary="Получение всех полезных привычек пользователя",
        return_dto=PydanticDTO[HabitReturnDTO],
    )
    async def get_user_habits(
        self,
        request: Request[UsernameSchema, TokenSchema, State],
        service: HabitService,
    ) -> Response[list[HabitReturnDTO]]:

        if not (habits := await service.get_all_habits(author=request.user.username)):
            raise HTTPException(
                status_code=status_codes.HTTP_404_NOT_FOUND,
                detail=f"У пользователя <{request.user.username}> еще нет полезных привычек",
            )

        resp = [HabitReturnDTO.model_validate(habit) for habit in habits]
        return Response(resp)

    @get(
        path="/statistics",
        summary="Получение статистики выполнения привычки",
        description="Метод возвращает метрики выполнения привычки в текущем периоде (скользящее окно) и общую статистику по привычке",
        return_dto=PydanticDTO[HabitStatisticsReturn],
    )
    async def get_user_habit_statistics(
        self,
        title: str,
        request: Request[UsernameSchema, TokenSchema, State],
        service: HabitService,
    ) -> Response[HabitStatisticsReturn]:

        try:
            habit, habit_dates = await service.get_current_period_habit_dates(
                title=title, author=request.user.username
            )
        except errors.HabitNotFoundError as exc:
            raise HTTPException(
                status_code=status_codes.HTTP_404_NOT_FOUND,
                detail=exc.message,
            )

        resp = HabitStatisticsReturn(
            title=habit.title,
            count=habit.count,
            period=habit.period,
            period_in_days=habit.period_in_days,
            current_count=len(habit_dates),
            dates_in_period=[habit_date.completed_at for habit_date in habit_dates],
            current_streak_start_date=habit.current_streak_start_date,
            current_streak_days=habit.current_streak_days,
            max_streak_days=habit.max_streak_days,
        )
        return Response(resp)
