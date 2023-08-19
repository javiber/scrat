"Module containing all Serializers"
import typing as T

from .base import Serializer
from .dill import DillSerializer  # noqa: F401
from .json import JsonSerializer  # noqa: F401
from .numpy import NumpySerializer
from .pandas import PandasSerializer
from .pickle import PickleSerializer

DEFAULT_SERIALIZERS = {
    "DataFrame": PandasSerializer,
    "Series": PandasSerializer,
    "ndarray": NumpySerializer,
}


def get_default_serializer(func: T.Callable) -> Serializer:
    """
    Try to find a sane serializer using the function's typehint.

    Defaults to `PickleSerializer`

    Parameters
    ----------
    func
        The user function to be called

    Returns
    -------
        An instance of the chosen Serializer
    """
    import inspect

    sign = inspect.signature(func)
    if hasattr(sign, "return_annotations"):
        return DEFAULT_SERIALIZERS.get(
            sign.return_annotation.__name__, PickleSerializer
        )()

    return PickleSerializer()


__all__ = [
    "Serializer",
    "PickleSerializer",
    "DillSerializer",
    "JsonSerializer",
    "NumpySerializer",
    "PandasSerializer",
]
