import pickle
import typing as T
from pathlib import Path


class PickleSerializer:
    def __init__(self) -> None:
        pass

    def dump(self, obj: T.Any, path: Path):
        with open(path, "wb") as f:
            pickle.dump(obj, f)

    def load(self, path: Path) -> T.Any:
        with open(path, "rb") as f:
            return pickle.load(f)
