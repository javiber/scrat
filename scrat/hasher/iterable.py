import logging
import typing as T

from scrat.utils import hash_method

from .base import Hasher

logger = logging.getLogger(__name__)


class IterableHasher(Hasher):
    def __init__(self, item_hasher: Hasher) -> None:
        super().__init__()
        self.item_hasher = item_hasher

    def hash(self, value: T.Iterable) -> str:
        return hash_method(*[self.item_hasher.hash(x) for x in value])
