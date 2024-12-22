import pytest
from sqlmodel import SQLModel

from vita.src.util.logg import Logg
from vita.src.util.sql_model import SQLSession


@pytest.fixture
def session() -> SQLSession:
    session = SQLSession(Logg(), "sqlite")
    SQLModel.metadata.drop_all(session.session.bind)
    SQLModel.metadata.create_all(session.session.bind)
    return session
