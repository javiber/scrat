import typing as T
from pathlib import Path

from .timer import Timer  # noqa

PathLike = T.Union[str, Path]


_SUFFIXES = list(reversed(list(enumerate(["B", "KB", "MB", "GB"]))))


def humanize_size(size: int) -> str:
    "Format file size in bytes into a human-readable string"
    base = 1024
    for exp, suffix in _SUFFIXES:
        if size >= base**exp:
            return f"{size/base**exp:.1f}{suffix}"
    raise ValueError("could not format int %s", int)
