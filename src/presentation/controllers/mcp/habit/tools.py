import json

from fastmcp import Context, FastMCP
from fastmcp.dependencies import CurrentContext, Depends

from application.schemas.auth import UserSchema
from application.schemas.habit import ExtendedHabitReturnDTO
from application.services.habit import HabitService
from presentation.dependencies_mcp import get_auth_user, get_habit_service


def register(mcp: FastMCP) -> None:
    """Регистрация всех инструментов habits"""

    @mcp.tool(
        description="Get habits completion data for analysis. Returns structured data with habits and their completion statistics for the last N days."
    )
    async def get_habits_overall(
        days: int = 30,
        ctx: Context = CurrentContext(),
        user: UserSchema = Depends(get_auth_user),
        habit_service: HabitService = Depends(get_habit_service),
    ) -> str:

        author = user.username

        await ctx.debug(f"Starting collecting habits information for {author=} with {days=}")

        habits = await habit_service.get_defined_period_extended_habits(
            author=author, limit_days=days
        )

        await ctx.debug(
            f"Finished collecting habits information for {author=} with {days=}. Collected {len(habits)} habits"
        )

        models = [ExtendedHabitReturnDTO.model_validate(habit).model_dump() for habit in habits]

        return json.dumps(
            {
                "days_analyzed": days,
                "total_habits": len(models),
                "habits": models,
                "schema": ExtendedHabitReturnDTO.model_json_schema(),
            },
            ensure_ascii=False,
            default=str,
        )
