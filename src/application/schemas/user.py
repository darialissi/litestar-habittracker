from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class UserDTO(BaseModel):
    """
    Схема модели User, валидирует ввод
    """

    username: str = Field(
        min_length=5,
        max_length=30,
        pattern="^[A-Za-z0-9-_]+$",
        description="Имя пользователя, может содержать только буквы, цифры, дефисы и нижние подчеркивания",
    )
    password: str = Field(min_length=5, description="Пароль пользователя")

    model_config = ConfigDict(from_attributes=True)


class UserReturnDTO(BaseModel):
    """
    Общая схема модели User, валидирует вывод
    """

    id: int = Field(description="ID пользователя")
    username: str = Field(description="Имя пользователя")
    created_at: datetime = Field(description="Дата создания пользователя")
    updated_at: datetime = Field(description="Дата последнего обновления пользователя")

    model_config = ConfigDict(from_attributes=True)
