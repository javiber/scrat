import pickle
import typing as T
from pathlib import Path


class PickleSerializer:
    """
    Pickle serializer.

    Parameters
    ----------
    dump_kwargs
        Extra arguments for pickle.dump, by default None
    load_kwargs
        Extra arguments for pickle.load, by default None
    """

    def __init__(
        self,
        dump_kwargs: T.Optional[T.Dict[str, T.Any]] = None,
        load_kwargs: T.Optional[T.Dict[str, T.Any]] = None,
    ) -> None:
        self.dump_kwargs = dump_kwargs if dump_kwargs is not None else {}
        self.load_kwargs = load_kwargs if load_kwargs is not None else {}

    def dump(self, obj: T.Any, path: Path):
        with open(path, "wb") as f:
            pickle.dump(obj, f, **self.dump_kwargs)

    def load(self, path: Path) -> T.Any:
        with open(path, "rb") as f:
            return pickle.load(f, **self.load_kwargs)
