from litestar import Litestar, Router
from litestar.openapi import OpenAPIConfig
from litestar.openapi.plugins import ScalarRenderPlugin

from infrastructure.database import create_tables, drop_tables, sqlalchemy_plugin
from presentation.controllers.habit import HabitController
from presentation.controllers.user import UserController

user_router = Router(
    path="/account",
    route_handlers=[UserController],
)

habit_router = Router(
    path="/habits",
    route_handlers=[HabitController],
)

all_routers = Router(
    path="/api",
    route_handlers=[user_router, habit_router],
)

app = Litestar(
    route_handlers=[all_routers],
    on_startup=[create_tables],
    on_shutdown=[drop_tables],
    plugins=[sqlalchemy_plugin],
    openapi_config=OpenAPIConfig(
        title="API",
        version="1.0.0",
        path="/docs",
        render_plugins=[ScalarRenderPlugin()],
    ),
)
