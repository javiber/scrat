import hashlib
import typing as T
from pathlib import Path

from .timer import Timer

PathLike = T.Union[str, Path]


def hash_method(*args) -> str:
    h = hashlib.md5(usedforsecurity=False)
    for value in args:
        if isinstance(value, str):
            value = value.encode()
        h.update(value)
    return h.hexdigest()


_SUFFIXES = reversed(list(enumerate(["B", "KB", "GB"])))


def humanize_size(size: int) -> str:
    base = 1024
    for exp, suffix in _SUFFIXES:
        if size >= base**exp:
            return f"{size/base**exp:.1f}{suffix}"
