import logging
import os
import typing as T
from datetime import datetime
from pathlib import Path

from sqlalchemy.sql import exists, select

from scrat.db import DBConnector, Entry

from .config import Config
from .hasher import Hasher, HashManager
from .serializer import Serializer

logger = logging.getLogger(__name__)


class Squirrel:
    def __init__(
        self,
        name: str,
        serializer: Serializer,
        hashers: T.Optional[T.Dict[str, Hasher]] = None,
        hash_code: T.Optional[bool] = True,
        ignore_args: T.Optional[T.List[str]] = None,
        watch_functions: T.Optional[T.List[T.Any]] = None,
        watch_globals: T.Optional[T.List[str]] = None,
        force: T.Optional[bool] = None,
        disable: T.Optional[bool] = None,
    ) -> None:
        self.config = Config.load()
        self.name = name
        self.force = force if force is not None else self.config.force
        self.disable = disable if disable is not None else self.config.disable
        self.db_connector = DBConnector(self.config.db_path)
        self.hash_manager = HashManager(
            hashers=hashers,
            ignore_args=ignore_args,
            hash_code=hash_code,
            watch_functions=watch_functions,
            watch_globals=watch_globals,
        )
        self.serializer = serializer

    def hash(
        self, args: T.List[T.Any], kwargs: T.Dict[str, T.Any], func: T.Callable
    ) -> str:
        hash_key = self.hash_manager.hash(args=args, kwargs=kwargs, func=func)
        logger.debug("Hash key for %s is '%s'", self.name, hash_key)
        return hash_key

    def exists(self, hash_key):
        if self.force or self.disable:
            logger.debug(
                "Forcing the result or scrat is disable, not reusing the result"
            )
            return False

        with self.db_connector.session() as session:
            return session.query(exists().where(Entry.hash == hash_key)).scalar()

    def fetch(self, hash_key):
        logger.debug("Fetching '%s' for %s", hash_key, self.name)

        with self.db_connector.session() as session:
            entry = session.scalar(select(Entry).where(Entry.hash == hash_key))
            result = self.serializer.load(Path(entry.path))
            entry.use_count = entry.use_count + 1
            entry.used_at = datetime.now()
            session.commit()
        return result

    def stash(self, hash_key: str, time_s: int, result: T.Any):
        if self.disable:
            logger.debug("Scrat is disable, not saving")
            return

        logger.debug("Storing '%s' for %s", hash_key, self.name)
        path = self.config.cache_path / f"{self.name}_{hash_key}"

        self.serializer.dump(result, path)
        file_size = round(os.stat(path).st_size)

        with self.db_connector.session() as session:
            entry = Entry(
                hash=hash_key,
                name=self.name,
                path=str(path),
                created_at=datetime.now(),
                used_at=None,
                size=file_size,
                use_count=0,
                time_s=time_s,
            )
            session.add(entry)
            session.commit()
