from typing import override

from model.graphql_input import SubAccountGraphqlInput
from model.graphql_type import SubAccountGraphqlType
from model.model import SubAccount
from util.err import VitaError
from util.sql_model import SQLSession

from .base_service import BaseService


class CreateSubAccountService(BaseService):

    def __init__(self, session: SQLSession):
        super().__init__(session)

    @override
    def execute(
        self, input: SubAccountGraphqlInput
    ) -> SubAccountGraphqlType | VitaError:

        sub_account = input.to_pydantic()
        sub_account.id = None

        try:
            result = self.session.save(SubAccount, sub_account, "system")
        except VitaError as e:
            return e

        return SubAccountGraphqlType.from_pydantic(result)