import typing as T
from pathlib import Path

if T.TYPE_CHECKING:
    import numpy as np


class NumpySerializer:
    def __init__(
        self,
        save_kwargs: T.Optional[T.Dict[str, T.Any]] = None,
        load_kwargs: T.Optional[T.Dict[str, T.Any]] = None,
    ) -> None:
        # test that numpy is installed
        import numpy  # noqa: F401

        self.save_kwargs = save_kwargs if save_kwargs is not None else {}
        self.load_kwargs = load_kwargs if load_kwargs is not None else {}

    def dump(self, obj: "np.ndarray", path: Path):
        import numpy

        numpy.save(path, obj, **self.save_kwargs)
        obj.save(path)

    def load(self, path: Path) -> "np.ndarray":
        import numpy

        return numpy.load(path, **self.load_kwargs)
