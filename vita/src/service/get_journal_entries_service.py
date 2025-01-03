from typing import override

from sqlmodel import select
from sqlalchemy.orm import joinedload

from vita.src.model.convert import GraphqlConvert
from vita.src.model.graphql_input import JournalEntriesGraphqlInput
from vita.src.model.graphql_type import JournalEntryGraphqlType
from vita.src.model.model import JournalEntry, InnerJournalEntry
from vita.src.util.condition import Condition, ConditionType
from vita.src.util.err import VitaError
from vita.src.util.sql_model import SQLSession

from .base_service import BaseService


class GetJournalEntriesService(BaseService):

    def __init__(self, session: SQLSession):
        super().__init__(session)

    @override
    def execute(
        self, input: JournalEntriesGraphqlInput
    ) -> list[JournalEntryGraphqlType] | VitaError:
        conditions = []

        if input.name:
            cond = Condition(JournalEntry.name, ConditionType.LIKE, input.name)
            conditions.append(cond.to_sqlachemy())

        if input.description:
            cond = Condition(
                JournalEntry.description, ConditionType.LIKE, input.description
            )
            conditions.append(cond.to_sqlachemy())

        if input.from_date:
            cond = Condition(
                JournalEntry.date, ConditionType.GREATER_THAN, input.from_date
            )
            conditions.append(cond.to_sqlachemy())

        if input.to_date:
            cond = Condition(JournalEntry.date, ConditionType.LESS_THAN, input.to_date)
            conditions.append(cond.to_sqlachemy())

        if input.status:
            cond = Condition(JournalEntry.status, ConditionType.EQUAL, input.status)
            conditions.append(cond.to_sqlachemy())

        if input.account_id:
            cond = Condition(
                InnerJournalEntry.account_id, ConditionType.EQUAL, input.account_id
            )
            conditions.append(cond.to_sqlachemy())

        if input.sub_account_id:
            cond = Condition(
                InnerJournalEntry.sub_account_id,
                ConditionType.EQUAL,
                input.sub_account_id,
            )
            conditions.append(cond.to_sqlachemy())

        query = (
            select(JournalEntry)
            .options(joinedload(JournalEntry.inner_journal_entries))
            .where(*conditions)
        )
        journal_entries = self.session.execute(query, JournalEntry, False, True)

        if not journal_entries:
            return VitaError(400, "Journal entry not found")

        return [
            GraphqlConvert.model_to_type(JournalEntryGraphqlType, journal_entry)
            for journal_entry in journal_entries
        ]
