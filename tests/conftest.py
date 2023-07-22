import os
from pathlib import Path
from tempfile import gettempdir

import pytest
from sqlalchemy import create_engine

from scrat import stash
from scrat.config import Config
from scrat.db import DBConnector


@pytest.fixture
def in_memory_engine():
    return create_engine("sqlite://")


@pytest.fixture
def patched_decorator(mocker, in_memory_engine):
    mocker.patch("scrat.db.connector.create_engine", lambda _: in_memory_engine)
    tmp_folder = gettempdir()
    mocker.patch(
        "scrat.config.Config.load", lambda *_: Config(base_path=Path(tmp_folder))
    )
    config = Config.load()
    os.makedirs(config.cache_path, exist_ok=True)
    DBConnector.create_db("")
    return stash
