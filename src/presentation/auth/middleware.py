from litestar.connection import ASGIConnection
from litestar.exceptions import NotAuthorizedException
from litestar.middleware import AbstractAuthenticationMiddleware, AuthenticationResult

from application.schemas.auth import TokenSchema, UserSchema
from application.services import errors
from application.services.auth import AuthService
from config import settings


class JWTAuthenticationMiddleware(AbstractAuthenticationMiddleware):

    def __init__(self, auth_service_instance: AuthService, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.auth_service_instance = auth_service_instance

    async def authenticate_request(self, connection: ASGIConnection) -> AuthenticationResult:

        token = connection.cookies.get(settings.AUTH_COOKIE)

        if not token:
            raise NotAuthorizedException(detail="You are unathorized!")

        try:
            token_decoded: TokenSchema = self.auth_service_instance.validate_token(token)
        except errors.TokenInvalidError as exc:
            raise NotAuthorizedException(detail=f"You are unathorized! {exc.message}")

        username = UserSchema(username=token_decoded.sub)

        return AuthenticationResult(user=username, auth=token)
