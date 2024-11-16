from jwt.exceptions import InvalidTokenError
from litestar.connection import ASGIConnection
from litestar.exceptions import NotAuthorizedException
from litestar.middleware import AbstractAuthenticationMiddleware, AuthenticationResult

from config import settings
from utils.auth.token import Token

from .schemas import TokenSchema, UsernameSchema


class JWTAuthenticationMiddleware(AbstractAuthenticationMiddleware):
    async def authenticate_request(self, connection: ASGIConnection) -> AuthenticationResult:

        token = connection.cookies.get(settings.AUTH_COOKIE)

        if not token:
            raise NotAuthorizedException(detail="You are unathorized!")

        try:
            decoded = Token.decode_jwt(private_key=settings.TOKEN_KEY_SECRET, token=token)
        except InvalidTokenError:
            raise NotAuthorizedException(detail="You are unathorized!")

        token_decoded = TokenSchema(**decoded)
        username = UsernameSchema(username=token_decoded.sub)

        return AuthenticationResult(user=username, auth=token)
