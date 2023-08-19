import typing as T
from abc import ABC, abstractmethod
from pathlib import Path


class Serializer(ABC):
    """
    Abstract class from which all Serializer inherit from.
    """

    @abstractmethod
    def dump(self, obj: T.Any, path: Path):
        """
        Save an object to disk.

        Parameters
        ----------
        obj
            The result to save.
        path
            The target location in the filesystem.
        """
        return NotImplemented

    @abstractmethod
    def load(self, path: Path) -> T.Any:
        """
        Load a saved object from disk.

        Parameters
        ----------
        path
            Location of the stored result.

        Returns
        -------
            The object loaded into memory.
        """
        return NotImplemented
