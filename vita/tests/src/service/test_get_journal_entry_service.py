from datetime import date
from vita.src.model.graphql_input import SingleGraphqlInput
from vita.src.model.model import (
    CreditDebitEnum,
    StatusEnum,
    JournalEntry,
    InnerJournalEntry,
)
from vita.src.service.get_journal_entry_service import GetJournalEntryService
from vita.src.util.constant import SYSTEM_USER
from vita.src.util.sql_model import SQLSession
from vita.src.model.convert import GraphqlConvert


def test_get_journal_entry_service_case01(session: SQLSession):
    entity = JournalEntry(
        name="name",
        description="description",
        date=date(2022, 1, 1),
        status=StatusEnum.FIXED,
    )
    entity = session.save(JournalEntry, entity, SYSTEM_USER)
    assert entity

    sub_entity = InnerJournalEntry(
        account_id="",
        sub_account_id="",
        journal_entry_id=entity.id,
        amount=1000,
        credit_debit=CreditDebitEnum.CREDIT,
        index=1,
    )
    sub_entity = session.save(InnerJournalEntry, sub_entity, SYSTEM_USER)
    assert sub_entity

    input = SingleGraphqlInput(id=entity.id)
    result = GetJournalEntryService(session).execute(input)

    journal_entry = GraphqlConvert.type_to_model(JournalEntry, result)

    assert journal_entry
    assert journal_entry.id == entity.id
    assert journal_entry.name
    assert journal_entry.name == entity.name
    assert journal_entry.description
    assert journal_entry.description == entity.description
    assert journal_entry.date == entity.date
    assert journal_entry.status == entity.status

    assert len(journal_entry.inner_journal_entries) == 1
    inner_journal_entry = journal_entry.inner_journal_entries[0]
    assert inner_journal_entry.journal_entry_id == sub_entity.journal_entry_id
    assert inner_journal_entry.amount == sub_entity.amount
    assert inner_journal_entry.credit_debit == sub_entity.credit_debit
    assert inner_journal_entry.index
    assert inner_journal_entry.index == sub_entity.index
