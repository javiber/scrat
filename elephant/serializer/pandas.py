import typing as T
from enum import Enum
from pathlib import Path


class Format(Enum):
    parquet = "parquet"
    csv = "csv"


class PandasSerializer:
    def __init__(self, format: T.Union[str, Format] = Format.parquet) -> None:
        self.format = format if isinstance(format, Format) else Format(format)

    def dump(self, obj: "DataFrame", path: Path):
        if self.format == Format.parquet:
            obj.to_parquet(path)

    def load(self, path: Path) -> "DataFrame":
        import pandas as pd

        if self.format == Format.parquet:
            pd.read_parquet(path)
