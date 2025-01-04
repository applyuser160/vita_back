from datetime import date
from vita.src.model.graphql_input import CollectJournalEntriesGraphqlInput
from vita.src.model.model import (
    CreditDebitEnum,
    StatusEnum,
    JournalEntry,
    InnerJournalEntry,
)
from vita.src.service.collect_journal_entries_service import (
    CollectJournalEntriesService,
)
from vita.src.util.constant import SYSTEM_USER
from vita.src.util.sql_model import SQLSession
from vita.src.model.convert import GraphqlConvert


def test_collect_journal_entries_service_case01(session: SQLSession):
    entities = [
        JournalEntry(
            id="id_1",
            name="name1",
            description="description1",
            date=date(2022, 1, 1),
            status=StatusEnum.FIXED,
        ),
        JournalEntry(
            id="id_2",
            name="name2",
            description="description2",
            date=date(2022, 1, 1),
            status=StatusEnum.RESOLVED,
        ),
        JournalEntry(
            id="id_3",
            name="name3",
            description="description3",
            date=date(2022, 1, 1),
            status=StatusEnum.UNFIXED,
        ),
    ]
    entities = session.bulk_save(entities, SYSTEM_USER)
    assert entities

    sub_entities = [
        InnerJournalEntry(
            id="id1",
            account_id="a",
            sub_account_id="",
            journal_entry_id=entities[0].id,
            amount=1000,
            credit_debit=CreditDebitEnum.CREDIT,
            index=1,
        ),
        InnerJournalEntry(
            id="id2",
            account_id="b",
            sub_account_id="",
            journal_entry_id=entities[0].id,
            amount=2000,
            credit_debit=CreditDebitEnum.CREDIT,
            index=2,
        ),
        InnerJournalEntry(
            id="id3",
            account_id="a",
            sub_account_id="",
            journal_entry_id=entities[1].id,
            amount=3000,
            credit_debit=CreditDebitEnum.CREDIT,
            index=1,
        ),
    ]
    sub_entities = session.bulk_save(sub_entities, SYSTEM_USER)
    assert sub_entities

    input = CollectJournalEntriesGraphqlInput(
        account_ids=["a"],
    )
    results = CollectJournalEntriesService(session).execute(input)

    inner_journal_entries = [
        GraphqlConvert.type_to_model(InnerJournalEntry, result) for result in results
    ]

    assert len(inner_journal_entries) == 2

    assert inner_journal_entries[0].id == sub_entities[0].id
    assert inner_journal_entries[0].journal_entry.id == entities[0].id

    assert inner_journal_entries[1].id == sub_entities[2].id
    assert inner_journal_entries[1].journal_entry.id == entities[1].id
