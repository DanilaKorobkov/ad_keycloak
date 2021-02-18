import attr

__all__ = (
    "ADKeycloakException",

    "PermissionDenied",
    "TokenValidationError",
)


class ADKeycloakException(Exception):
    pass


@attr.s(auto_attribs=True, slots=True, frozen=True)
class PermissionDenied(ADKeycloakException):
    app: str
    perm: str


class TokenValidationError(ADKeycloakException):
    pass
