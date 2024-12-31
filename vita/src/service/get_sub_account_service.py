from typing import override

from sqlmodel import select
from sqlalchemy.orm import joinedload

from vita.src.model.convert import GraphqlConvert
from vita.src.model.graphql_input import SingleGraphqlInput
from vita.src.model.graphql_type import SubAccountGraphqlType
from vita.src.model.model import SubAccount
from vita.src.util.err import VitaError
from vita.src.util.sql_model import SQLSession

from .base_service import BaseService


class GetSubAccountService(BaseService):

    def __init__(self, session: SQLSession):
        super().__init__(session)

    @override
    def execute(self, input: SingleGraphqlInput) -> SubAccountGraphqlType | VitaError:
        query = (
            select(SubAccount)
            .options(joinedload(SubAccount.account))
            .where(SubAccount.id == input.id)
        )
        sub_account = self.session.execute(query, SubAccount, True, True)

        if not sub_account:
            return VitaError(400, "Account not found")
        elif isinstance(sub_account, list):
            return VitaError(400, "Account not found")

        return GraphqlConvert.model_to_type(SubAccountGraphqlType, sub_account)
