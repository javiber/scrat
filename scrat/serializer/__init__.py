from .base import Serializer  # NoQA
from .pandas import PandasSerializer
from .pickle import PickleSerializer

DEFAULT_SERIALIZERS = {"DataFrame": PandasSerializer()}


def get_default_serializer(func):
    import inspect

    sign = inspect.signature(func)
    if hasattr(sign, "return_annotations"):
        return DEFAULT_SERIALIZERS.get(
            sign.return_annotation.__name__, PickleSerializer()
        )

    return PickleSerializer()
