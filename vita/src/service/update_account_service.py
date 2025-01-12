from typing import override

from vita.src.model.graphql_input import AccountGraphqlInput
from vita.src.model.graphql_type import AccountGraphqlType, VitaErrorGraphqlType
from vita.src.model.model import Account
from vita.src.util.constant import SYSTEM_USER
from vita.src.util.err import VitaError
from vita.src.util.sql_model import SQLSession

from .base_service import BaseService


class UpdateAccountService(BaseService):

    def __init__(self, session: SQLSession):
        super().__init__(session)

    @override
    def execute(
        self, input: AccountGraphqlInput
    ) -> AccountGraphqlType | VitaErrorGraphqlType:

        account = input.to_pydantic()  # type: ignore

        try:
            result = self.session.save(Account, account, SYSTEM_USER)
        except VitaError as e:
            return VitaErrorGraphqlType(error_code=e.error_code, message=e.message)

        return AccountGraphqlType.from_pydantic(result)  # type: ignore
