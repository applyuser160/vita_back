from typing import override

from vita.src.model.convert import GraphqlConvert
from vita.src.model.graphql_input import JournalEntryGraphqlInput
from vita.src.model.graphql_type import JournalEntryGraphqlType, VitaErrorGraphqlType
from vita.src.model.model import InnerJournalEntry, JournalEntry
from vita.src.util.constant import SYSTEM_USER
from vita.src.util.err import VitaError
from vita.src.util.sql_model import SQLSession

from .base_service import BaseService


class UpdateJournalEntryService(BaseService):

    def __init__(self, session: SQLSession):
        super().__init__(session)

    @override
    def execute(
        self, input: JournalEntryGraphqlInput
    ) -> JournalEntryGraphqlType | VitaErrorGraphqlType:

        journal_entry = GraphqlConvert.input_to_model(JournalEntry, input)

        inner_journal_entries = GraphqlConvert.copy_models(
            journal_entry.inner_journal_entries
        )
        journal_entry = GraphqlConvert.copy_model(journal_entry)

        try:
            result = self.session.save(JournalEntry, journal_entry, SYSTEM_USER)
            if not result or not result.id:
                return VitaErrorGraphqlType(
                    error_code=500, message="Failed to create journal entry"
                )

            inner_result = [
                self.session.save(InnerJournalEntry, inner_journal_entry, SYSTEM_USER)
                for inner_journal_entry in inner_journal_entries
            ]
        except VitaError as e:
            return VitaErrorGraphqlType(error_code=e.error_code, message=e.message)

        result.inner_journal_entries = [i for i in inner_result if i]
        if not result:
            return VitaErrorGraphqlType(
                error_code=500, message="Failed to create journal entry"
            )

        return GraphqlConvert.model_to_type(JournalEntryGraphqlType, result)
