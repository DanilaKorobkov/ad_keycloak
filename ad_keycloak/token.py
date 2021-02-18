import typing as t

import attr
from marshmallow import EXCLUDE, Schema, fields, post_load, pre_load

__all__ = (
    "Token",
    "TokenSchema",
)


@attr.s(auto_attribs=True, slots=True, frozen=True)
class Token:
    client_id: str
    client_host: str
    preferred_username: str

    jwt_id: str
    issuer: str
    subject: str
    audience: t.FrozenSet[str]
    authorized_party: str


class TokenSchema(Schema):
    client_id = fields.Str(required=True, data_key="clientId")
    client_host = fields.Str(required=True, data_key="clientHost")
    preferred_username = fields.Str(required=True)

    jwt_id = fields.Str(required=True, data_key="jti")
    issuer = fields.Str(required=True, data_key="iss")
    subject = fields.Str(required=True, data_key="sub")
    authorized_party = fields.Str(required=True, data_key="azp")
    audience = fields.List(fields.Str, required=True, data_key="aud")

    @pre_load
    def aud_is_list_always(self, in_data: t.Dict, **_) -> t.Dict:
        value = in_data["aud"]
        if isinstance(value, str):
            in_data["aud"] = [value]
        return in_data

    @post_load
    def release(self, data: t.Dict, **_) -> Token:
        data["audience"] = frozenset(data["audience"])
        return Token(**data)

    class Meta:
        unknown = EXCLUDE
