from typing import override

from vita.src.model.convert import GraphqlConvert
from vita.src.model.graphql_input import JournalEntryGraphqlInput
from vita.src.model.graphql_type import JournalEntryGraphqlType
from vita.src.model.model import InnerJournalEntry, JournalEntry
from vita.src.util.constant import SYSTEM_USER
from vita.src.util.err import VitaError
from vita.src.util.sql_model import SQLSession

from .base_service import BaseService


class CreateJournalEntryService(BaseService):

    def __init__(self, session: SQLSession):
        super().__init__(session)

    @override
    def execute(
        self, input: JournalEntryGraphqlInput
    ) -> JournalEntryGraphqlType | VitaError:

        journal_entry = GraphqlConvert.input_to_model(JournalEntry, input)
        journal_entry.id = None
        inner_journal_entries = GraphqlConvert.copy_models(
            journal_entry.inner_journal_entries
        )

        try:
            result = self.session.save(JournalEntry, journal_entry, SYSTEM_USER)
            if not result or not result.id:
                return VitaError(500, "Failed to create journal entry")

            for inner_journal_entry in inner_journal_entries:
                inner_journal_entry.journal_entry_id = result.id

            inner_result = [
                self.session.save(InnerJournalEntry, inner_journal_entry, SYSTEM_USER)
                for inner_journal_entry in inner_journal_entries
            ]
        except VitaError as e:
            return e

        result.inner_journal_entries = [i for i in inner_result if i]
        if not result:
            return VitaError(500, "Failed to create journal entry")

        return GraphqlConvert.model_to_type(JournalEntryGraphqlType, result)
