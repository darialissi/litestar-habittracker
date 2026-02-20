from fastmcp import FastMCP


def register(mcp: FastMCP) -> None:
    """Регистрация всех промптов habits"""

    @mcp.prompt(description="Prompt for analyzing habit tracking data")
    def habits_analysis(days: int = 30) -> str:
        return f"""
        You are a habit tracking analyst. Your task is to analyze the user's habit data and provide insights.

        When you receive the habit data, please analyze:
            - Overall progress and trends
            - Peak productivity periods
            - Streak analysis  
            - Patterns in completion rates
            - Suggestions for improvement
            - Recommendations for optimization

        Focus on: dates, streaks, completion rates, and overall progress patterns.

        Use the get_habits_overall tool to fetch the actual habit data for the last {days} days.
        """

    @mcp.prompt(description="Prompt for weekly review of habits")
    def weekly_review() -> str:
        return """
        Conduct a weekly review of user's habits with diagrams and insights.
        
        Response format:

        Week in Numbers
        - How many days all habits were completed
        - Best day of the week
        
        Progress
        - Compare with last week
        - Which habits have improved
        
        Plans for Next Week
        - What needs improvement
        - Specific steps
        
        Use the get_habits_overall tool to fetch the actual habit data for the last 7 days.
        """
