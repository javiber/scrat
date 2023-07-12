import functools
import logging
import typing as T

from .cache import CacheManager
from .hasher.manager import HashManager
from .serializer import Serializer, get_default_serializer

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

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            hash_key = hash_manager.hash(args, kwargs, func)

            if _cacher.exists(hash_key):
                logger.info("Cache hit %s", hash_key)
                return _serializer.load(_cacher.get(hash_key))

            logger.info("Cache miss %s", hash_key)
            result = func(*args, **kwargs)

            path = _cacher.new(hash_key)
            _serializer.dump(result, path)
            _cacher.add(hash_key, path)

            return result

        return wrapper

    return deco
