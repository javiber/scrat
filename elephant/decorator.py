import functools
import logging
import os
import typing as T
from datetime import datetime

from .cache import CacheManager
from .db import Entry
from .hasher.manager import HashManager
from .serializer import Serializer, get_default_serializer
from .utils import Timer

logger = logging.getLogger(__name__)


def remember(
    serializer: T.Optional[Serializer] = None,
    hashers=None,
    name=None,
):
    def deco(func):
        hash_manager = HashManager(
            hashers=hashers, name=name if name is not None else func.__name__
        )
        _serializer = (
            serializer if serializer is not None else get_default_serializer(func)
        )
        _cacher = CacheManager()

        timer = Timer()

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            hash_key = hash_manager.hash(args, kwargs, func)

            if _cacher.exists(hash_key):
                logger.info("Cache hit %s", hash_key)
                return _serializer.load(_cacher.get(hash_key))

            logger.info("Cache miss %s", hash_key)
            timer.start()
            result = func(*args, **kwargs)
            func_time = timer.end()
            path = _cacher.new(hash_key)
            _serializer.dump(result, path)
            file_size = round(os.stat(path).st_size / (1024 * 1024))

            entry = Entry(
                hash=hash_key,
                name=hash_manager.name,
                path=str(path),
                created_at=datetime.now(),
                used_at=None,
                size_mb=file_size,
                use_count=0,
                time_s=func_time,
            )
            _cacher.add(entry)

            return result

        return wrapper

    return deco
