from typing import override

from sqlmodel import select
from sqlalchemy.orm import joinedload

from vita.src.model.convert import GraphqlConvert
from vita.src.model.graphql_input import SubAccountsGraphqlInput
from vita.src.model.graphql_type import SubAccountGraphqlType
from vita.src.model.model import SubAccount
from vita.src.util.err import VitaError
from vita.src.util.sql_model import SQLSession
from vita.src.util.condition import Condition, ConditionType

from .base_service import BaseService


class GetSubAccountsService(BaseService):

    def __init__(self, session: SQLSession):
        super().__init__(session)

    @override
    def execute(
        self, input: SubAccountsGraphqlInput
    ) -> list[SubAccountGraphqlType] | VitaError:
        conditions = []
        if input.name:
            cond = Condition(SubAccount.name, ConditionType.LIKE, input.name)
            conditions.append(cond.to_sqlachemy())

        if input.description:
            cond = Condition(
                SubAccount.description, ConditionType.LIKE, input.description
            )
            conditions.append(cond.to_sqlachemy())

        if input.account_id:
            cond = Condition(
                SubAccount.account_id, ConditionType.LIKE, input.account_id
            )
            conditions.append(cond.to_sqlachemy())

        query = (
            select(SubAccount)
            .options(joinedload(SubAccount.account))
            .where(*conditions)
        )
        sub_accounts = self.session.execute(query, SubAccount, False, True)

        if not sub_accounts:
            return VitaError(400, "Sub account not found")

        return [
            GraphqlConvert.model_to_type(SubAccountGraphqlType, sub_account)
            for sub_account in sub_accounts
        ]
