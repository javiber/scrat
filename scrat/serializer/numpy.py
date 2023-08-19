import typing as T
from pathlib import Path

if T.TYPE_CHECKING:
    import numpy as np


class NumpySerializer:
    """
    Serializer for numpy arrays.

    In order to use this Serializer numpy needs to be installed.


    Parameters
    ----------
    save_kwargs
        Extra arguments for numpy.save, by default None
    load_kwargs
        Extra arguments for numpy.load, by default None
    """

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
