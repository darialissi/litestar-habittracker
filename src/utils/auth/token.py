from datetime import datetime, timedelta, timezone

import jwt


class Token:

    @staticmethod
    def encode_jwt(
        payload: dict,
        private_key: str,
        expire: timedelta,
    ) -> str:
        to_encode = payload.copy()
        now = datetime.now(timezone.utc)
        expire = now + expire
        to_encode.update(
            exp=expire,
            iat=now,
        )
        encoded = jwt.encode(
            to_encode,
            private_key,
            algorithm="HS256",
        )
        return encoded

    @staticmethod
    def decode_jwt(
        token: str,
        private_key: str,
    ) -> dict:
        try:
            return jwt.decode(token, private_key, algorithms=["HS256"])
        except jwt.exceptions.InvalidTokenError:
            raise
