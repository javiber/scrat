import typing as T

from scrat.utils import hash_method

from .base import Hasher


class PandasHasher(Hasher):
    def __init__(self, use_values: bool = True) -> None:
        super().__init__()
        self.use_values = use_values

    def hash(self, value: T.Any) -> str:
        if self.use_values:
            return hash_method(value.index.values, value.values)
        return hash_method(value.index.values)
