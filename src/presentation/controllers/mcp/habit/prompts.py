from fastmcp import FastMCP


def register(mcp: FastMCP) -> None:
    """Регистрация всех промптов habits"""

    @mcp.prompt(description="Template for weekly review of habits")
    def weekly_review() -> str:
        return """
        Conduct a weekly review of my habits with diagrams and insights based on the data provided by the 'get_habits_overall' tool.
        
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
        
        Use data from my habits for analysis.
        """
