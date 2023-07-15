from pathlib import Path
from tempfile import gettempdir

import pytest
from sqlalchemy import create_engine

from elephant import remember


@pytest.fixture
def in_memory_engine():
    return create_engine("sqlite://")


@pytest.fixture
def patched_decorator(mocker, in_memory_engine):
    mocker.patch("elephant.db.create_engine", lambda _: in_memory_engine)
    mocker.patch("elephant.cache.CacheConfig.cache_path", Path(gettempdir()))
    return remember
