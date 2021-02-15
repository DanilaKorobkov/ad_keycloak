from abc import ABC, abstractmethod

__all__ = (
    "IIdentityProvider",
)


class IIdentityProvider(ABC):

    @abstractmethod
    def decode(self, token: str) -> None:
        pass

    @abstractmethod
    def has_perm(self, app: str, perm: str) -> bool:
        pass
