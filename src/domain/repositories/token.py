from abc import ABC, abstractmethod

from application.schemas.auth import AuthSchema


class ITokenRepository(ABC):
    """
    Интерфейс для хранилища токенов
    """

    @abstractmethod
    def save(self, auth_result: AuthSchema) -> None:
        """Сохранить результат аутентификации"""
        pass

    @abstractmethod
    def get(self) -> AuthSchema | None:
        """Получить результат аутентификации"""
        pass

    @abstractmethod
    def is_authenticated(self) -> bool:
        """Проверить наличие активной аутентификации"""
        pass

    @abstractmethod
    def clear(self) -> None:
        """Очистить сохраненную аутентификацию"""
        pass

    @abstractmethod
    def get_token(self) -> str | None:
        """Получить только токен"""
        pass
