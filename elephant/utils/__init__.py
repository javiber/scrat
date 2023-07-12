import hashlib
import typing as T
from pathlib import Path

PathLike = T.Union[str, Path]


def hash_method(*args) -> str:
    h = hashlib.sha1()
    for value in args:
        if isinstance(value, str):
            value = value.encode()
        h.update(value)
    return h.hexdigest()
