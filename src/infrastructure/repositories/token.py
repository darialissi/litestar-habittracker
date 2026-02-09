from application.schemas.auth import AuthSchema
from domain.repositories.token import ITokenRepository


class InMemoryTokenRepository(ITokenRepository):
    """
    Реализация хранилища токенов в памяти (для STDIO)
    """

    def __init__(self):
        """Приватное хранилище в памяти процесса"""
        self._auth_result: AuthSchema | None = None

    def save(self, auth_result: AuthSchema) -> None:
        self._auth_result = auth_result

    def get(self) -> AuthSchema | None:
        return self._auth_result

    def is_authenticated(self) -> bool:
        return self._auth_result is not None

    def clear(self) -> None:
        self._auth_result = None

    def get_token(self) -> str | None:
        if self._auth_result:
            return self._auth_result.token
        return None
