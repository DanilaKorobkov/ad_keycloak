import typing as t

import attr
from keycloak import KeycloakOpenID

from .exceptions import PermissionDenied
from .token import Token, TokenSchema

__all__ = (
    "KeycloakClient",
)


@attr.s(auto_attribs=True, slots=True, frozen=True)
class KeycloakClient:
    _open_id: KeycloakOpenID

    async def validate(self, token: str, app: str, perm: str) -> Token:
        decoded_token = self._decode(token)
        validate_perm(decoded_token, app, perm)

        builder = TokenSchema()
        return builder.load(decoded_token)

    def _decode(self, token: str) -> t.Dict:
        options = {
            'require_aud': True,
            'require_iat': True,
            'require_exp': True,
            'require_iss': True,
            'require_sub': True,
            'require_jti': True,
        }
        return self._open_id.decode_token(
            token,
            key=self._get_public_key(),
            options=options,
        )

    def _get_public_key(self) -> str:
        public_key = self._open_id.public_key()
        return get_wrapped_public_key(public_key)


def validate_perm(token: t.Dict, app: str, perm: str):
    try:
        permissions = token["resource_access"][app]["roles"]
        if perm in permissions:
            return
    except KeyError:
        pass
    raise PermissionDenied(app, perm)


def get_wrapped_public_key(key: str) -> str:
    return f"-----BEGIN PUBLIC KEY-----\n{key}\n-----END PUBLIC KEY-----"
