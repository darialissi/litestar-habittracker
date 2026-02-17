from presentation.controllers.mcp.factory import create_mcp_server

mcp = create_mcp_server()


if __name__ == "__main__":
    mcp.run(transport="stdio", log_level="DEBUG")
