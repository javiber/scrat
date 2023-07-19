from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .models import Base


class DBConnector:
    @classmethod
    def create_db(cls, path):
        engine = create_engine("sqlite:///" + str(path))
        Base.metadata.create_all(engine)

    def __init__(self, path) -> None:
        self.engine = create_engine("sqlite:///" + str(path))
        Base.metadata.create_all(self.engine)
        self.session_maker = sessionmaker(self.engine)

    def session(self) -> Session:
        return self.session_maker()
