import logging
import pytest
from sqlmodel import SQLModel

from vita.src.util.logg import Logg
from vita.src.util.sql_model import SQLSession


@pytest.fixture
def session() -> SQLSession:
    logg = Logg()
    logg.logger.level = logging.DEBUG
    session = SQLSession(logg, "sqlite")
    SQLModel.metadata.drop_all(session.session.bind)
    SQLModel.metadata.create_all(session.session.bind)
    return session
