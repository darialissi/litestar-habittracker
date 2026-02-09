from datetime import timedelta

import jwt
import pytest

from utils.auth.password import Password
from utils.auth.token import Token


@pytest.mark.unit
class TestAuth:
    @pytest.mark.parametrize(
        "password",
        [
            "ddddd55555",
            "1111111112222",
        ],
    )
    def test_hash(self, password: str):
        hashed = Password.hash_password(password)

        assert Password.validate_password(password, hashed) is True

    @pytest.mark.parametrize(
        "payload, private_key, expire",
        [
            ({"sub": "username"}, "PRIVATE_KEY", timedelta(minutes=10)),
            pytest.param(
                {"sub": "username"},
                "PRIVATE_KEY",
                timedelta(seconds=0),
                marks=pytest.mark.xfail(raises=ValueError),
            ),
        ],
    )
    def test_jwt(self, payload: dict, private_key: str, expire: timedelta):
        token = Token.encode_jwt(payload, private_key, expire)

        decoded = Token.decode_jwt(token, private_key)

        assert decoded.get("sub") == payload.get("sub")
