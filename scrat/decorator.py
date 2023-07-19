import functools
import logging
import typing as T

from scrat import Squirrel

from .hasher import Hasher
from .serializer import Serializer, get_default_serializer
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
):
    """Wraps a function to stash the results

    Parameters
    ----------
    serializer, optional
        Select a serializer for the function's result, by default `PickleSerializer`
        is used
    name, optional
        Name that identifies this function, by default the function __name__ is used
    hashers, optional
        Dictionary specifying hashers used for the argiments, by default None
    hash_code, optional
        Control if the function's code should be used in the hash, by default True
    ignore_args, optional
        List of arguments to ignore from the hash, by default None
    watch_functions, optional
        List of functions which code will be included in the hash, by default None
    watch_globals, optional
        List of global variables to include in the hash, by default None
    force, optional
        If set to True the saved result is ignored, the function called and the result
        overritten, by default the value on `scrat.Setting.force` is used
    disable, optional
        If set to True the saved result is ignored, the function called and the new
        result is also ignored, by default the value on `scrat.Setting.disable` is used
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
