from abc import ABC, abstractmethod
from typing import Any

from vita.src.util.err import VitaError
from vita.src.util.sql_model import SQLSession


class BaseService(ABC):

    def __init__(self, session: SQLSession):
        self.session = session

    @abstractmethod
    def execute(self, input: Any) -> Any | VitaError:
        return NotImplementedError()

    def get_logg(self):
        return self.logg
