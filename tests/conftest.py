from pathlib import Path
from tempfile import gettempdir

import pytest
from sqlalchemy import create_engine

from scrat import stash
from scrat.db import DBConnector


@pytest.fixture
def in_memory_engine():
    return create_engine("sqlite://")


@pytest.fixture
def patched_decorator(mocker, in_memory_engine):
    mocker.patch("scrat.db.connector.create_engine", lambda _: in_memory_engine)
    mocker.patch("scrat.config.Config.cache_path", Path(gettempdir()))
    DBConnector.create_db("")
    return stash
