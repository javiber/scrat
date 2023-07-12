import typing as T

from elephant.utils import hash_method

from .base import Hasher


class NumpyHasher(Hasher):
    def hash(self, value: T.Any) -> str:
        return hash_method(value)
