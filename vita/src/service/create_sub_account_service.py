from typing import override

from vita.src.model.graphql_input import SubAccountGraphqlInput
from vita.src.model.graphql_type import SubAccountGraphqlType, VitaErrorGraphqlType
from vita.src.model.model import SubAccount
from vita.src.util.constant import SYSTEM_USER
from vita.src.util.err import VitaError
from vita.src.util.sql_model import SQLSession

from .base_service import BaseService


class CreateSubAccountService(BaseService):

    def __init__(self, session: SQLSession):
        super().__init__(session)

    @override
    def execute(
        self, input: SubAccountGraphqlInput
    ) -> SubAccountGraphqlType | VitaErrorGraphqlType:

        sub_account = input.to_pydantic()  # type: ignore
        sub_account.id = None

        try:
            result = self.session.save(SubAccount, sub_account, SYSTEM_USER)
        except VitaError as e:
            return VitaErrorGraphqlType(error_code=e.error_code, message=e.message)

        return SubAccountGraphqlType.from_pydantic(result)  # type: ignore
