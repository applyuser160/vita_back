from typing import override

from sqlalchemy import func
from sqlmodel import select

from vita.src.model.convert import GraphqlConvert
from vita.src.model.graphql_input import CollectJournalEntriesGraphqlInput
from vita.src.model.graphql_type import DailyBalanceGraphqlType
from vita.src.model.model import DailyBalance, JournalEntry, InnerJournalEntry
from vita.src.util.condition import Condition, ConditionType
from vita.src.util.sql_model import SQLSession

from .base_service import BaseService


class CalculateDailyBalanceService(BaseService):

    def __init__(self, session: SQLSession):
        super().__init__(session)

    @override
    def execute(
        self, input: CollectJournalEntriesGraphqlInput
    ) -> list[DailyBalanceGraphqlType]:
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

        balances: list[DailyBalance] = []

        if account_conditions:
            query = (
                select(
                    InnerJournalEntry.account_id,
                    InnerJournalEntry.sub_account_id,
                    JournalEntry.date,
                    func.sum(InnerJournalEntry.amount).label("total_amount"),
                )
                .join(InnerJournalEntry.journal_entry)
                .where(*account_conditions)
                .group_by(
                    InnerJournalEntry.account_id,
                    JournalEntry.date,
                )
            )

            balances.extend(
                [
                    DailyBalance(
                        account_id=i[0],
                        sub_account_id=i[1],
                        date=i[2],
                        total_amount=i[3],
                    )
                    for i in self.session.session.exec(query).all()
                ]
            )

        if sub_account_conditions:
            query = (
                select(
                    InnerJournalEntry.account_id,
                    InnerJournalEntry.sub_account_id,
                    JournalEntry.date,
                    func.sum(InnerJournalEntry.amount).label("total_amount"),
                )
                .join(InnerJournalEntry.journal_entry)
                .where(*sub_account_conditions)
                .group_by(
                    InnerJournalEntry.sub_account_id,
                    JournalEntry.date,
                )
            )

            balances.extend(
                [
                    DailyBalance(
                        account_id=i[0],
                        sub_account_id=i[1],
                        date=i[2],
                        total_amount=i[3],
                    )
                    for i in self.session.session.exec(query).all()
                ]
            )

        if not balances:
            return []

        return [
            GraphqlConvert.model_to_type(DailyBalanceGraphqlType, balance)
            for balance in balances
        ]
