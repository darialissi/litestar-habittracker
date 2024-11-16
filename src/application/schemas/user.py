from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class UserDTO(BaseModel):
    """
    Схема модели User, валидирует ввод
    """

    username: str = Field(min_length=5, max_length=30, pattern="^[A-Za-z0-9-_]+$")
    password: str = Field(min_length=5)

    model_config = ConfigDict(from_attributes=True)


class UserReturnDTO(BaseModel):
    """
    Общая схема модели User, валидирует вывод
    """

    id: int
    username: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
