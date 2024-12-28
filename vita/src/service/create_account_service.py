from typing import override

from vita.src.model.graphql_input import AccountGraphqlInput
from vita.src.model.graphql_type import AccountGraphqlType
from vita.src.model.model import Account
from vita.src.util.err import VitaError
from vita.src.util.sql_model import SQLSession

from .base_service import BaseService


class CreateAccountService(BaseService):

    def __init__(self, session: SQLSession):
        super().__init__(session)

    @override
    def execute(self, input: AccountGraphqlInput) -> AccountGraphqlType | VitaError:

        account = input.to_pydantic()  # type: ignore
        account.id = None

        try:
            result = self.session.save(Account, account, "system")
        except VitaError as e:
            return e

        return AccountGraphqlType.from_pydantic(result)  # type: ignore
