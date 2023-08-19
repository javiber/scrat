import typing as T

from .base import Hasher


class PandasHasher(Hasher):
    """
    Hasher for Pandas Series and DataFrames

    Parameters
    ----------
    use_values
        If False, only the index of the dataframe is included in the hash
        This can help with the speed of the hasher on big dataframes where
        you only care what rows are included but you know the values
        don't change, by default True
    """

    def __init__(self, use_values: bool = True) -> None:
        super().__init__()
        self.use_values = use_values

    def hash(self, value: T.Any) -> str:
        if self.use_values:
            return self.md5_hash(value.index.values, value.values)
        return self.md5_hash(value.index.values)
