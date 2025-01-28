from typing import override

from vita.src.model.convert import GraphqlConvert
from vita.src.model.graphql_input import AccountGraphqlInput
from vita.src.model.graphql_type import AccountGraphqlType, VitaErrorGraphqlType
from vita.src.model.model import Account
from vita.src.util.constant import SYSTEM_USER
from vita.src.util.err import VitaError
from vita.src.util.sql_model import SQLSession

from .base_service import BaseService


class CreateAccountService(BaseService):

    def __init__(self, session: SQLSession):
        super().__init__(session)

    @override
    def execute(
        self, input: AccountGraphqlInput
    ) -> AccountGraphqlType | VitaErrorGraphqlType:

        account = GraphqlConvert.input_to_model(Account, input)
        account.id = None

        try:
            result = self.session.save(Account, account, SYSTEM_USER)
            self.session.session.refresh(result)
        except VitaError as e:
            return VitaErrorGraphqlType(error_code=e.error_code, message=e.message)

        print(result)
        print(type(result))

        if not result:
            return VitaErrorGraphqlType(error_code=400, message="Not found")

        return GraphqlConvert.model_to_type(AccountGraphqlType, result)
