import inspect
import typing as T
from collections import OrderedDict
from hashlib import sha1

from .base import Hasher
from .to_string import ToStringHasher


class HashManager:
    def __init__(
        self,
        name: T.Optional[str],
        hashers: T.Optional[T.Dict[str, Hasher]] = None,
        hash_code: T.Optional[bool] = True,
    ) -> None:
        # TODO: enforce unique names
        self.name = name
        self.hash_code = hash_code
        self.hashers: T.Dict[str, Hasher] = hashers if hashers is not None else {}

    def hash(
        self, args: T.List[T.Any], kwargs: T.Dict[str, T.Any], func: T.Callable
    ) -> str:
        hashed_args = []
        for arg_name, arg in self._normalize_args(args, kwargs, func):
            hasher = self._get_hasher(arg_name, arg)
            hashed_args.append(hasher.hash(arg))
        hash_result = self._combine_hashes(hashed_args)
        if self.hash_code:
            hash_result = self._combine_hashes([hash_result, self._hash_code(func)])

        return "_".join([self.name, hash_result])

    def _get_hasher(self, arg_name: str, arg: T.Any) -> Hasher:
        if arg_name in self.hashers:
            return self.hashers[arg_name]
        # TODO: class defaults?
        return ToStringHasher()

    def _combine_hashes(self, hashes: T.List[str]) -> str:
        return "".join(hashes)

    def _hash_code(self, func) -> str:
        return sha1(inspect.getsource(func).encode()).hexdigest()

    def _normalize_args(
        self, args: T.List[T.Any], kwargs: T.Dict[str, T.Any], func: T.Callable
    ):
        normalized_args = OrderedDict()

        sign = inspect.signature(func)

        for arg_name, param in sign.parameters.items():
            if param.kind == param.POSITIONAL_ONLY:
                # Value must be supplied as a positional argument.
                # Python has no explicit syntax for defining positional-only parameters, but many built-in and extension module functions (especially those that accept only one or two parameters) accept them.
                normalized_args[arg_name] = args.pop(0)
            elif param.kind == param.POSITIONAL_OR_KEYWORD:
                # Value may be supplied as either a keyword or positional argument (this is the standard binding behaviour for functions implemented in Python.)
                if arg_name in kwargs:
                    normalized_args[arg_name] = kwargs[arg_name]
                elif len(args) > 0:
                    normalized_args[arg_name] = args.pop(0)
                else:
                    normalized_args[arg_name] = param.default

            elif param.kind == param.VAR_POSITIONAL:
                # A tuple of positional arguments that aren’t bound to any other parameter. This corresponds to a *args parameter in a Python function definition.
                for i, arg in enumerate(args):
                    normalized_args[f"#{i}"] = arg
                arg = []
            elif param.kind == param.KEYWORD_ONLY:
                # Value must be supplied as a keyword argument. Keyword only parameters are those which appear after a * or *args entry in a Python function definition.
                normalized_args[arg_name] = kwargs[arg_name]
            if param.kind == param.VAR_KEYWORD:
                # A dict of keyword arguments that aren’t bound to any other parameter. This corresponds to a **kwargs parameter in a Python function definition.
                if arg_name in kwargs:
                    normalized_args[arg_name] = kwargs[arg_name]
                else:
                    normalized_args[arg_name] = param.default
        return normalized_args
