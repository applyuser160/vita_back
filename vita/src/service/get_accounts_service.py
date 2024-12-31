from typing import override

from sqlmodel import select
from sqlalchemy.orm import joinedload

from vita.src.model.convert import GraphqlConvert
from vita.src.model.graphql_input import AccountsGraphqlInput
from vita.src.model.graphql_type import AccountGraphqlType
from vita.src.model.model import Account
from vita.src.util.err import VitaError
from vita.src.util.sql_model import SQLSession
from vita.src.util.condition import Condition, ConditionType

from .base_service import BaseService


class GetAccountsService(BaseService):

    def __init__(self, session: SQLSession):
        super().__init__(session)

    @override
    def execute(
        self, input: AccountsGraphqlInput
    ) -> list[AccountGraphqlType] | VitaError:
        conditions = []
        if input.name:
            cond = Condition(Account.name, ConditionType.LIKE, input.name)
            conditions.append(cond.to_sqlachemy())

        if input.description:
            cond = Condition(Account.description, ConditionType.LIKE, input.description)
            conditions.append(cond.to_sqlachemy())

        if input.dept:
            cond = Condition(Account.dept, ConditionType.EQUAL, input.dept)
            conditions.append(cond.to_sqlachemy())

        if input.bs_pl:
            cond = Condition(Account.bs_pl, ConditionType.EQUAL, input.bs_pl)
            conditions.append(cond.to_sqlachemy())

        if input.credit_debit:
            cond = Condition(
                Account.credit_debit, ConditionType.EQUAL, input.credit_debit
            )
            conditions.append(cond.to_sqlachemy())

        query = (
            select(Account).options(joinedload(Account.sub_accounts)).where(*conditions)
        )
        accounts = self.session.execute(query, Account, False, True)

        if not accounts:
            return VitaError(400, "Account not found")

        return [
            GraphqlConvert.model_to_type(AccountGraphqlType, account)
            for account in accounts
        ]
