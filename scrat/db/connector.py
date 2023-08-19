from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from scrat.utils import PathLike

from .models import Base


class DBConnector:
    """
    Wrapper to handle the connection to sqlite.

    Parameters
    ----------
    path
        Path to the sqlite file.
    """

    def __init__(self, path: PathLike) -> None:
        self.engine = create_engine("sqlite:///" + str(path))
        Base.metadata.create_all(self.engine)
        self.session_maker = sessionmaker(self.engine)

    @classmethod
    def create_db(cls, path: PathLike):
        """
        Initialize the database.

        Parameters
        ----------
        path
            Path to the sqlite file.
        """
        engine = create_engine("sqlite:///" + str(path))
        Base.metadata.create_all(engine)

    def session(self) -> Session:
        """
        Create a session

        Returns
        -------
            SQLAlchemy's session
        """
        return self.session_maker()
