import functools
import logging
import typing as T

from .config import CachePolicy
from .hasher import Hasher
from .serializer import Serializer, get_default_serializer
from .squirrel import Squirrel
from .utils import Timer

logger = logging.getLogger(__name__)


def stash(
    serializer: T.Optional[Serializer] = None,
    name: T.Optional[str] = None,
    hashers: T.Optional[T.Dict[str, Hasher]] = None,
    hash_code: T.Optional[bool] = True,
    ignore_args: T.Optional[T.List[str]] = None,
    watch_functions: T.Optional[T.List[T.Any]] = None,
    watch_globals: T.Optional[T.List[str]] = None,
    force: T.Optional[bool] = None,
    disable: T.Optional[bool] = None,
    max_size: T.Optional[int] = None,
    cache_policy: CachePolicy = CachePolicy.lru,
):
    """Wrap a function to stash the results

    Parameters
    ----------
    serializer
        Select a serializer for the function's result, by default a good
        serializer is inferred from the typehint, using `PickleSerializer` as
        the fallback.
    name
        Name that identifies this function, by default the function name is used.
    hashers
        Dictionary specifying hashers used for the arguments, by default hashers
        are selected according to the type of the argument, using `ToStringHasher`
        as the fallback.
    hash_code
        Control if the function's code should be used in the hash, by default True.
    ignore_args
        List of arguments to ignore from the hash, by default None
    watch_functions
        List of functions which code should be included in the hash, by default None
    watch_globals
        List of global variables to include in the hash, by default None
    force
        If set to True the stash is ignored, the function is called and the result
        is saved to the stash, by default the global setting `scrat.Setting.force` is
        used
    disable
        If set to True the stash is ignored, the function called and the result
        is **not** saved, by default the global setting `scrat.Setting.disable` is used
    max_size
        Maximum size allowed for files of this function, if the limit is about to be met
        other files are removed befor storing a new one based on the cache_policy
    cache_policy
        Cache policy, by default Least Recentrly Used (LRU) is applied

    Notes
    -----
    If possible, avoid using the default `PickleSerializer`. This serializer is used by
    default because it works with most objects but pickle is not a good format to store
    the results long-term. We encourage users to select one the other serializers
    provided or writing a custom one.

    Examples
    --------

    Simple example

    >>> import scrat as sc
    >>> @sc.stash()
    >>> def funcion():
    >>>     return 1

    Custom serializer

    >>> @sc.stash(serializer=sc.JsonSerializer())
    >>> def funcion():
    >>>     return {"json": True}
    """

    def deco(func):
        squirrel = Squirrel(
            hashers=hashers,
            name=name if name is not None else func.__name__,
            ignore_args=ignore_args,
            hash_code=hash_code,
            watch_functions=watch_functions,
            watch_globals=watch_globals,
            serializer=serializer
            if serializer is not None
            else get_default_serializer(func),
            force=force,
            disable=disable,
            max_size=max_size,
            cache_policy=cache_policy,
        )

        timer = Timer()

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            hash_key = squirrel.hash(args, kwargs, func)
            if squirrel.exists(hash_key):
                logger.info("Cache hit %s", hash_key)
                return squirrel.fetch(hash_key)

            logger.info("Cache miss %s", hash_key)
            timer.start()
            result = func(*args, **kwargs)
            func_time = timer.end()

            squirrel.stash(hash_key=hash_key, time_s=func_time, result=result)

            return result

        return wrapper

    return deco
