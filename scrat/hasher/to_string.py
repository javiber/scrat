import typing as T

from .base import Hasher


class ToStringHasher(Hasher):
    def hash(self, value: T.Any) -> str:
        return str(value)
