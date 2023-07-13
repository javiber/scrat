import inspect
import logging
import typing as T
from collections import OrderedDict
from collections.abc import Iterable

from elephant.utils import hash_method

from .base import Hasher
from .iterable import IterableHasher
from .numpy import NumpyHasher
from .pandas import PandasHasher
from .to_string import ToStringHasher

logger = logging.getLogger(__name__)


FALLBACK = ToStringHasher()
DEFAULTS = OrderedDict()
try:
    import numpy as np

    DEFAULTS[np.ndarray] = NumpyHasher()
except ImportError:
    logger.debug("numpy not installed, NumpyHasher disabled")
try:
    import pandas as pd

    DEFAULTS[pd.DataFrame] = PandasHasher()
    DEFAULTS[pd.Series] = PandasHasher()
except ImportError:
    logger.debug("numpy not installed, NumpyHasher disabled")

DEFAULTS[list] = IterableHasher(FALLBACK)
DEFAULTS[tuple] = IterableHasher(FALLBACK)


class HashManager:
    def __init__(
        self,
        name: T.Optional[str],
        hashers: T.Optional[T.Dict[str, Hasher]] = None,
        hash_code: T.Optional[bool] = True,
    ) -> None:
        # TODO: enforce unique names?
        self.name = name
        self.hash_code = hash_code
        self.hashers: T.Dict[str, Hasher] = hashers if hashers is not None else {}

    def hash(
        self, args: T.List[T.Any], kwargs: T.Dict[str, T.Any], func: T.Callable
    ) -> str:
        # hash arguments
        hashed_args = []
        for arg_name, arg in self._normalize_args(args, kwargs, func).items():
            hasher = self._get_hasher(arg_name, arg)
            logger.debug(
                "using '%s' for argument '%s'", hasher.__class__.__name__, arg_name
            )
            hashed_value = hasher.hash(arg)
            hashed_args.append(hash_method(arg_name, hashed_value, type(arg).__name__))
        hash_result = hash_method(*hashed_args)
        logger.debug("%s arguments hash: '%s'", self.name, hash_result)

        # hash funcion's code if necessary
        if self.hash_code:
            hashed_code = self._hash_code(func)
            hash_result = hash_method(hash_result, hashed_code)
            logger.debug("%s code hash: '%s'", self.name, hashed_code)

        # prepend name for traceability
        hash_result = "_".join([self.name, hash_result])
        logger.debug("%s final hash: '%s'", self.name, hash_result)
        return hash_result

    def _get_hasher(self, arg_name: str, arg: T.Any) -> Hasher:
        if arg_name in self.hashers:
            return self.hashers[arg_name]
        for cls, hasher in DEFAULTS.items():
            if isinstance(arg, cls):
                return hasher
        return FALLBACK

    def _hash_code(self, func) -> str:
        return hash_method(inspect.getsource(func).encode())

    def _normalize_args(
        self, args: T.List[T.Any], kwargs: T.Dict[str, T.Any], func: T.Callable
    ):
        args = list(args)
        normalized_args = OrderedDict()

        sign = inspect.signature(func)

        for arg_name, param in sign.parameters.items():
            if param.kind == param.POSITIONAL_ONLY:
                # NOTE: Value must be supplied as a positional argument.
                #       Python has no explicit syntax for defining positional-only parameters,
                #       but many built-in and extension module functions (especially those that
                #       accept only one or two parameters) accept them.
                normalized_args[arg_name] = args.pop(0)
            elif param.kind == param.POSITIONAL_OR_KEYWORD:
                # NOTE: Value may be supplied as either a keyword or positional argument.
                #       This is the standard binding behaviour for functions implemented in Python.
                if arg_name in kwargs:
                    normalized_args[arg_name] = kwargs[arg_name]
                elif len(args) > 0:
                    normalized_args[arg_name] = args.pop(0)
                else:
                    normalized_args[arg_name] = param.default

            elif param.kind == param.VAR_POSITIONAL:
                # NOTE: A tuple of positional arguments that aren’t bound to any other parameter.
                #       This corresponds to a *args parameter in a Python function definition.

                # consume all remainder args
                for i, arg in enumerate(args):
                    normalized_args[f"*{i}"] = arg
                args = []
            elif param.kind == param.KEYWORD_ONLY:
                # NOTE: Value must be supplied as a keyword argument.
                #       Keyword only parameters are those which appear after a * or *args entry
                #       in a Python function definition.
                # If the param is keyword only then it must be passed as a kwarg, however
                # we are not enforncing it here so that we don't fail and instead the user gets the normal
                # python error
                normalized_args[arg_name] = kwargs.get(arg_name)
            if param.kind == param.VAR_KEYWORD:
                # NOTE: A dict of keyword arguments that aren’t bound to any other parameter.
                #       This corresponds to a **kwargs parameter in a Python function definition.

                # consume all remainder kwargs
                for arg_name, arg in kwargs.items():
                    normalized_args[f"**{arg_name}"] = arg
                kwargs = {}
        return normalized_args
