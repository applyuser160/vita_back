from abc import ABC, abstractmethod
from typing import Any

from util.err import VitaError
from util.sql_model import SQLSession


class BaseService(ABC):

    def __init__(self, session: SQLSession):
        self.session = session

    @abstractmethod
    def execute(self, input: Any) -> Any | VitaError:
        return NotImplementedError()

    def get_logg(self):
        return self.logg
