from pydantic import BaseModel, Field


class ResponseSchema(BaseModel):
    """
    Общая схема Response
    """

    errors: list[str] = Field(
        description="Список ошибок, возникших при обработке запроса",
        default=[],
    )
    payload: dict = Field(description="Полезная нагрузка", default={})
