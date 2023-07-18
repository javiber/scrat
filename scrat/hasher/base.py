import typing as T
from abc import ABC, abstractmethod


class Hasher(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def hash(self, value: T.Any) -> str:
        return NotImplemented
