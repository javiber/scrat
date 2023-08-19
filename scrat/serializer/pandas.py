import typing as T
from enum import Enum
from pathlib import Path

if T.TYPE_CHECKING:
    import pandas as pd


class Format(Enum):
    parquet = "parquet"
    hdf5 = "hdf5"
    feather = "feather"
    orc = "orc"
    excel = "excel"
    csv = "csv"
    pickle = "pickle"
    json = "json"
    stata = "stata"


class PandasSerializer:
    """
    Serializer for Pandas Series and DataFrames.

    In order to use this Serializer pandas needs to be installed,
    some formats might need aditional libraries.

    Parameters
    ----------
    format
        Serialization method from the ones supported by pandas,
        by default Format.parquet
    to_kwargs
        Extra arguments for the corresponding pandas.read_<format> function,
        by default None
    read_kwargs
        Extra arguments for the corresponding pandas.to_<format> function,
        by default None
    """

    def __init__(
        self,
        format: T.Union[str, Format] = Format.parquet,
        to_kwargs: T.Optional[T.Dict[str, T.Any]] = None,
        read_kwargs: T.Optional[T.Dict[str, T.Any]] = None,
    ) -> None:
        # test that pandas is installed
        import pandas  # noqa: F401

        self.format = format if isinstance(format, Format) else Format(format)

        self.to_kwargs = to_kwargs if to_kwargs is not None else {}
        self.read_kwargs = read_kwargs if read_kwargs is not None else {}

    def dump(self, obj: "pd.DataFrame", path: Path):
        to_method = getattr(obj, f"to_{self.format.value}")
        to_method(path, **self.to_kwargs)

    def load(self, path: Path) -> "pd.DataFrame":
        import pandas

        read_method = getattr(pandas, f"read_{self.format.value}")
        return read_method(path, **self.read_kwargs)
