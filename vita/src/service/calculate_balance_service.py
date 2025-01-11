from typing import override

from sqlmodel import select, func

from vita.src.model.convert import GraphqlConvert
from vita.src.model.graphql_input import CollectJournalEntriesGraphqlInput
from vita.src.model.graphql_type import BalanceGraphqlType
from vita.src.model.model import Balance, JournalEntry, InnerJournalEntry
from vita.src.util.condition import Condition, ConditionType
from vita.src.util.sql_model import SQLSession

from .base_service import BaseService


class CalculateBalanceService(BaseService):

    def __init__(self, session: SQLSession):
        super().__init__(session)

    @override
    def execute(
        self, input: CollectJournalEntriesGraphqlInput
    ) -> list[BalanceGraphqlType]:
        account_conditions = []
        sub_account_conditions = []

        if input.account_ids:
            cond = Condition(
                InnerJournalEntry.account_id,
                ConditionType.IN,
                input.account_ids,
            )
            account_conditions.append(cond.to_sqlachemy())

        if input.sub_account_ids:
            cond = Condition(
                InnerJournalEntry.sub_account_id,
                ConditionType.IN,
                input.sub_account_ids,
            )
            sub_account_conditions.append(cond.to_sqlachemy())

        if input.from_date:
            cond = Condition(
                JournalEntry.date,
                ConditionType.GREATER_THAN,
                input.from_date,
            )
            account_conditions.append(cond.to_sqlachemy())
            sub_account_conditions.append(cond.to_sqlachemy())

        if input.to_date:
            cond = Condition(
                JournalEntry.date,
                ConditionType.LESS_THAN,
                input.to_date,
            )
            account_conditions.append(cond.to_sqlachemy())
            sub_account_conditions.append(cond.to_sqlachemy())

        balances: list[Balance] = []

        if account_conditions:
            query = (
                select(
                    InnerJournalEntry.account_id,
                    InnerJournalEntry.sub_account_id,
                    func.sum(InnerJournalEntry.amount).label("total_amount"),
                )
                .join(InnerJournalEntry.journal_entry)
                .where(*account_conditions)
                .group_by(
                    InnerJournalEntry.account_id,
                )
            )

            balances.extend(
                [
                    Balance(account_id=i[0], sub_account_id=i[1], total_amount=i[2])
                    for i in self.session.session.exec(query).all()
                ]
            )

        if sub_account_conditions:
            query = (
                select(
                    InnerJournalEntry.account_id,
                    InnerJournalEntry.sub_account_id,
                    func.sum(InnerJournalEntry.amount).label("total_amount"),
                )
                .join(InnerJournalEntry.journal_entry)
                .where(*sub_account_conditions)
                .group_by(
                    InnerJournalEntry.sub_account_id,
                )
            )

            balances.extend(
                [
                    Balance(account_id=i[0], sub_account_id=i[1], total_amount=i[2])
                    for i in self.session.session.exec(query).all()
                ]
            )

        if not balances:
            return []

        return [
            GraphqlConvert.model_to_type(BalanceGraphqlType, balance)
            for balance in balances
        ]
