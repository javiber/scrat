import typing as T
from abc import ABC, abstractmethod
from pathlib import Path


class Serializer(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def dump(self, obj: T.Any, path: Path):
        return NotImplemented

    @abstractmethod
    def load(self, path: Path) -> T.Any:
        return NotImplemented
