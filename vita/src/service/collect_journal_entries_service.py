from typing import override

from sqlmodel import select
from sqlalchemy.orm import joinedload

from vita.src.model.convert import GraphqlConvert
from vita.src.model.graphql_input import CollectJournalEntriesGraphqlInput
from vita.src.model.graphql_type import InnerJournalEntryGraphqlType
from vita.src.model.model import JournalEntry, InnerJournalEntry
from vita.src.util.condition import Condition, ConditionType
from vita.src.util.sql_model import SQLSession

from .base_service import BaseService


class CollectJournalEntriesService(BaseService):

    def __init__(self, session: SQLSession):
        super().__init__(session)

    @override
    def execute(
        self, input: CollectJournalEntriesGraphqlInput
    ) -> list[InnerJournalEntryGraphqlType]:
        conditions = []

        if input.account_ids:
            cond = Condition(
                InnerJournalEntry.account_id,
                ConditionType.IN,
                input.account_ids,
            )
            conditions.append(cond.to_sqlachemy())

        if input.sub_account_ids:
            cond = Condition(
                InnerJournalEntry.sub_account_id,
                ConditionType.IN,
                input.sub_account_ids,
            )
            conditions.append(cond.to_sqlachemy())

        if input.from_date:
            cond = Condition(
                JournalEntry.target_date,
                ConditionType.GREATER_THAN,
                input.from_date,
            )
            conditions.append(cond.to_sqlachemy())

        if input.to_date:
            cond = Condition(
                JournalEntry.target_date,
                ConditionType.LESS_THAN,
                input.to_date,
            )
            conditions.append(cond.to_sqlachemy())

        query = (
            select(InnerJournalEntry)
            .options(joinedload(InnerJournalEntry.journal_entry))
            .where(*conditions)
        )

        inner_journal_entries = self.session.execute(
            query, InnerJournalEntry, False, True
        )

        if not inner_journal_entries:
            return []

        return [
            GraphqlConvert.model_to_type(
                InnerJournalEntryGraphqlType, inner_journal_entry
            )
            for inner_journal_entry in inner_journal_entries
        ]
