import typing as T
from enum import Enum
from pathlib import Path


class Format(Enum):
    parquet = "parquet"
    csv = "csv"


class PandasSerializer:
    def __init__(self, format: T.Union[str, Format] = Format.parquet) -> None:
        self.format = format if isinstance(format, Format) else Format(format)

    def dump(self, obj: T.Any, path: Path):
        if self.format == Format.parquet:
            obj.to_parquet(path)
        elif self.format == Format.csv:
            obj.to_csv(path)

    def load(self, path: Path) -> T.Any:
        import pandas as pd  # noqa

        if self.format == Format.parquet:
            df = pd.read_parquet(path)
        elif self.format == Format.csv:
            df = pd.read_csv(path)

        return df
