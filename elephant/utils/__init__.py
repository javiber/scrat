import hashlib
import typing as T
from pathlib import Path

PathLike = T.Union[str, Path]


def hash_method(*args) -> str:
    h = hashlib.sha1()
    for value in args:
        h.update(value)
    return h.hexdigest()
