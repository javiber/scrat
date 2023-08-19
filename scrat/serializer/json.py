import json
import typing as T
from pathlib import Path


class JsonSerializer:
    def __init__(
        self,
        dump_kwargs: T.Optional[T.Dict[str, T.Any]] = None,
        load_kwargs: T.Optional[T.Dict[str, T.Any]] = None,
    ) -> None:
        self.dump_kwargs = dump_kwargs if dump_kwargs is not None else {}
        self.load_kwargs = load_kwargs if load_kwargs is not None else {}

    def dump(self, obj: T.Any, path: Path):
        with open(path, "wb") as f:
            json.dump(obj, f, **self.dump_kwargs)

    def load(self, path: Path) -> T.Any:
        with open(path, "rb") as f:
            return json.load(f, **self.load_kwargs)
