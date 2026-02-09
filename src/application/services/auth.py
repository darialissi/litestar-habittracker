from datetime import timedelta

from application.schemas.auth import AuthSchema, TokenSchema, UserCred, UserSchema
from application.services import errors
from domain.repositories.token import ITokenRepository
from utils.auth.password import Password
from utils.auth.token import Token


class AuthService:

    def __init__(self, secret_key: str, expired_minutes: int, repo: ITokenRepository | None = None):
        self.secret_key = secret_key
        self.expired_minutes = expired_minutes
        self.token_repo = repo

    def create_token(self, username: str) -> AuthSchema:

        payload = {"sub": username}
        token = Token.encode_jwt(
            payload,
            private_key=self.secret_key,
            expire=timedelta(minutes=self.expired_minutes),
        )
        auth_result = AuthSchema(token=token, user=UserSchema(username=username))

        return auth_result

    def create_and_save_token(self, username: str) -> AuthSchema:

        auth_result = self.create_token(username=username)

        self.token_repo.save(auth_result)

        return auth_result

    def validate_token(self, token: str) -> TokenSchema:

        try:
            decoded = Token.decode_jwt(private_key=self.secret_key, token=token)
        except ValueError:
            raise errors.TokenInvalidError(token=token)

        return TokenSchema(**decoded)

    def hash_password(self, password: str) -> str:
        return Password.hash_password(password)

    def is_valid_password(self, password: str, hashed_password: str) -> bool:

        if Password.validate_password(password=password, hashed_password=hashed_password):
            return True

        return False

    def auth_user(self, cred: UserCred) -> AuthSchema | None:
        if not self.is_valid_password(password=cred.password, hashed_password=cred.hashed_password):
            return None

        if self.token_repo is not None:
            return self.create_and_save_token(username=cred.username)

        return self.create_token(username=cred.username)
