import typing as T
from pathlib import Path


class DillSerializer:
    def __init__(
        self,
        dump_kwargs: T.Optional[T.Dict[str, T.Any]] = None,
        load_kwargs: T.Optional[T.Dict[str, T.Any]] = None,
    ) -> None:
        # test that dill is installed
        import dill  # noqa: F401

        self.dump_kwargs = dump_kwargs if dump_kwargs is not None else {}
        self.load_kwargs = load_kwargs if load_kwargs is not None else {}

    def dump(self, obj: T.Any, path: Path):
        import dill

        with open(path, "wb") as f:
            dill.dump(obj, f, **self.dump_kwargs)

    def load(self, path: Path) -> T.Any:
        import dill

        with open(path, "rb") as f:
            return dill.load(f, **self.load_kwargs)
