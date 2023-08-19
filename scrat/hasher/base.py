import hashlib
import typing as T
from abc import ABC, abstractmethod


class Hasher(ABC):
    "Abstract class from which all Hashers inherit from"

    @abstractmethod
    def hash(self, value: T.Any) -> str:
        """Calculate the hash-string corresponding to a value

        Parameters
        ----------
        value
            The argument value

        Returns
        -------
            The hash-string
        """
        return NotImplemented

    @classmethod
    def md5_hash(cls, *args) -> str:
        """
        Generate the hash for strings and bytes using md5

        Returns
        -------
            the resulting hexdigest
        """
        h = hashlib.md5()
        for value in args:
            if isinstance(value, str):
                value = value.encode()
            h.update(value)
        return h.hexdigest()
