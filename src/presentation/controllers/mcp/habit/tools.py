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
        description="Analysis of habits completion for the last N days. Default period is last 30 days."
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

        data = json.dumps(
            {"schema": ExtendedHabitReturnDTO.model_json_schema(), "habits": models},
            ensure_ascii=False,
            default=str,
        )

        return f"""I need you to analyze my habit tracking data and provide insights for the last {days} days.

        AGGREGATED DATA: {data}
        
        Provide insights including:
        - Overall progress and trends
        - Peak productivity periods
        - Streak analysis
        - Patterns in completion rates
        - Suggestions for improvement
        - Recommendations for optimization
        
        Focus on: dates, streaks, completion rates, and overall progress patterns.
        """
