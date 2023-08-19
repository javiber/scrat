import logging
import typing as T

from .base import Hasher

logger = logging.getLogger(__name__)


class IterableHasher(Hasher):
    """
    Apply one Hasher to each element of a iterable

    Parameters
    ----------
    item_hasher
        A Hasher to hash each value in the iterable

    Examples
    --------
    >>> import scrat as sc
    >>> import numpy as np
    >>> hasher = sc.IterableHasher(sc.NumpyHasher())
    >>> hasher.hash([np.zeros(5), np.ones(3)])
    'f86f4d4c12a426ce5d54d715723584be'
    """

    def __init__(self, item_hasher: Hasher) -> None:
        super().__init__()
        self.item_hasher = item_hasher

    def hash(self, value: T.Iterable) -> str:
        return self.md5_hash(*[self.item_hasher.hash(x) for x in value])
