from abc import ABC, abstractmethod
from typing import Any

from vita.src.model.graphql_type import VitaErrorGraphqlType
from vita.src.util.sql_model import SQLSession


class BaseService(ABC):

    def __init__(self, session: SQLSession):
        self.session = session

    @abstractmethod
    def execute(self, input: Any) -> Any | VitaErrorGraphqlType:
        return NotImplementedError()

    def get_logg(self):
        return self.logg
