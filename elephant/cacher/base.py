from pathlib import Path
from abc import ABC, abstractmethod


class Cacher(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def add(self, path: Path):
        return NotImplemented

    @abstractmethod
    def new(self, hash: str) -> Path:
        return NotImplemented
