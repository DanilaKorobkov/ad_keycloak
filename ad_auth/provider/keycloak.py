import typing as t

import attr
from keycloak import KeycloakOpenID

from .i_provider import IIdentityProvider

__all__ = (
    "Keycloak",
)


@attr.s(auto_attribs=True)
class Keycloak(IIdentityProvider):
    _open_id: KeycloakOpenID
    _token_data: t.Dict = attr.ib(init=False)

    def decode(self, token: str) -> None:
        options = {
            'require_aud': True,
            'require_iat': True,
            'require_exp': True,
            'require_iss': True,
            'require_sub': True,
            'require_jti': True,
        }
        self._token_data = self._open_id.decode_token(
            token,
            key=self._get_public_key(),
            options=options,
        )

    def has_perm(self, app: str, perm: str) -> bool:
        try:
            permissions = self._token_data["resource_access"][app]["roles"]
            if perm in permissions:
                return True
        except KeyError:
            pass
        return False

    def _get_public_key(self) -> str:
        public_key = self._open_id.public_key()
        return get_wrapped_public_key(public_key)


def get_wrapped_public_key(key: str) -> str:
    return f"-----BEGIN PUBLIC KEY-----\n{key}\n-----END PUBLIC KEY-----"
