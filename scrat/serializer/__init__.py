from .base import Serializer  # noqa: F401
from .dill import DillSerializer  # noqa: F401
from .json import JsonSerializer
from .numpy import NumpySerializer
from .pandas import PandasSerializer
from .pickle import PickleSerializer

DEFAULT_SERIALIZERS = {
    "DataFrame": PandasSerializer,
    "Series": PandasSerializer,
    "ndarray": NumpySerializer,
}


def get_default_serializer(func):
    import inspect

    sign = inspect.signature(func)
    if hasattr(sign, "return_annotations"):
        return DEFAULT_SERIALIZERS.get(
            sign.return_annotation.__name__, PickleSerializer
        )()

    return PickleSerializer()
