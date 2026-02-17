from fastmcp import FastMCP


def create_mcp_server() -> FastMCP:
    """Фабрика для создания и настройки MCP сервера"""
    mcp = FastMCP(name="mcp-habittracker")

    # Импортируем и регистрируем обработчики
    from .habit import prompts, tools

    tools.register(mcp)
    prompts.register(mcp)

    return mcp
