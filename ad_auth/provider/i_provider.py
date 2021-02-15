from abc import ABC, abstractmethod

import attr

__all__ = (
    "IIdentityProvider",
)


@attr.s(auto_attribs=True)
class IIdentityProvider(ABC):

    @abstractmethod
    def decode(self, token: str) -> None:
        pass

    @abstractmethod
    def has_perm(self, app: str, perm: str) -> bool:
        pass
