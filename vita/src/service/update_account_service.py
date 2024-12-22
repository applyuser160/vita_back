from typing import override

from model.graphql_input import AccountGraphqlInput
from model.graphql_type import AccountGraphqlType
from model.model import Account
from util.err import VitaError
from util.sql_model import SQLSession

from .base_service import BaseService


class UpdateAccountService(BaseService):

    def __init__(self, session: SQLSession):
        super().__init__(session)

    @override
    def execute(self, input: AccountGraphqlInput) -> AccountGraphqlType | VitaError:

        account = input.to_pydantic()

        try:
            result = self.session.save(Account, account, "system")
        except VitaError as e:
            return e

        return AccountGraphqlType.from_pydantic(result)
