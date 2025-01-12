from typing import override

from sqlmodel import select
from sqlalchemy.orm import joinedload

from vita.src.model.convert import GraphqlConvert
from vita.src.model.graphql_input import SingleGraphqlInput
from vita.src.model.graphql_type import JournalEntryGraphqlType, VitaErrorGraphqlType
from vita.src.model.model import JournalEntry
from vita.src.util.sql_model import SQLSession

from .base_service import BaseService


class GetJournalEntryService(BaseService):

    def __init__(self, session: SQLSession):
        super().__init__(session)

    @override
    def execute(
        self, input: SingleGraphqlInput
    ) -> JournalEntryGraphqlType | VitaErrorGraphqlType:
        query = (
            select(JournalEntry)
            .options(joinedload(JournalEntry.inner_journal_entries))
            .where(JournalEntry.id == input.id)
        )
        journal_entry = self.session.execute(query, JournalEntry, True, True)

        if not journal_entry:
            return VitaErrorGraphqlType(
                error_code=400, message="Journal entry not found"
            )
        elif isinstance(journal_entry, list):
            return VitaErrorGraphqlType(
                error_code=400, message="Journal entry not found"
            )

        return GraphqlConvert.model_to_type(JournalEntryGraphqlType, journal_entry)
