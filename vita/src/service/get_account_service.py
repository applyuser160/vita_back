from typing import override

from sqlmodel import select
from sqlalchemy.orm import joinedload

from vita.src.model.convert import GraphqlConvert
from vita.src.model.graphql_input import SingleGraphqlInput
from vita.src.model.graphql_type import AccountGraphqlType, VitaErrorGraphqlType
from vita.src.model.model import Account
from vita.src.util.sql_model import SQLSession

from .base_service import BaseService


class GetAccountService(BaseService):

    def __init__(self, session: SQLSession):
        super().__init__(session)

    @override
    def execute(
        self, input: SingleGraphqlInput
    ) -> AccountGraphqlType | VitaErrorGraphqlType:
        query = (
            select(Account)
            .options(joinedload(Account.sub_accounts))
            .where(Account.id == input.id)
        )
        account = self.session.execute(query, Account, True, True)

        if not account:
            return VitaErrorGraphqlType(error_code=400, message="Account not found")
        elif isinstance(account, list):
            return VitaErrorGraphqlType(error_code=400, message="Account not found")

        return GraphqlConvert.model_to_type(AccountGraphqlType, account)
