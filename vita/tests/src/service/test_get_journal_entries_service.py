from datetime import date
from vita.src.model.graphql_input import JournalEntriesGraphqlInput
from vita.src.model.model import (
    CreditDebitEnum,
    StatusEnum,
    JournalEntry,
    InnerJournalEntry,
)
from vita.src.service.get_journal_entries_service import GetJournalEntriesService
from vita.src.util.constant import SYSTEM_USER
from vita.src.util.sql_model import SQLSession
from vita.src.model.convert import GraphqlConvert


def test_get_journal_entries_service_case01(session: SQLSession):
    entities = [
        JournalEntry(
            name="name1",
            description="description1",
            target_date=date(2022, 1, 1),
            status=StatusEnum.FIXED,
        ),
        JournalEntry(
            name="name2",
            description="description2",
            target_date=date(2022, 1, 1),
            status=StatusEnum.RESOLVED,
        ),
        JournalEntry(
            name="name3",
            description="description3",
            target_date=date(2022, 1, 1),
            status=StatusEnum.UNFIXED,
        ),
    ]
    entities = session.bulk_save(entities, SYSTEM_USER)
    assert entities

    sub_entities = [
        InnerJournalEntry(
            id="id1",
            account_id="",
            sub_account_id="",
            journal_entry_id=entities[0].id,
            amount=1000,
            credit_debit=CreditDebitEnum.CREDIT,
            index=1,
        ),
        InnerJournalEntry(
            id="id2",
            account_id="",
            sub_account_id="",
            journal_entry_id=entities[0].id,
            amount=2000,
            credit_debit=CreditDebitEnum.CREDIT,
            index=2,
        ),
        InnerJournalEntry(
            id="id3",
            account_id="",
            sub_account_id="",
            journal_entry_id=entities[1].id,
            amount=3000,
            credit_debit=CreditDebitEnum.CREDIT,
            index=1,
        ),
    ]
    sub_entities = session.bulk_save(sub_entities, SYSTEM_USER)
    assert sub_entities

    input = JournalEntriesGraphqlInput()
    results = GetJournalEntriesService(session).execute(input)

    journal_entries = [
        GraphqlConvert.type_to_model(JournalEntry, result) for result in results
    ]

    assert len(journal_entries) == 3

    journal_entry = journal_entries[0]
    entity = entities[0]
    assert journal_entry.id == entity.id
    assert journal_entry.name
    assert journal_entry.name == entity.name
    assert journal_entry.description
    assert journal_entry.description == entity.description
    assert journal_entry.target_date == entity.target_date
    assert journal_entry.status == entity.status

    assert len(journal_entry.inner_journal_entries) == 2
    assert (
        journal_entry.inner_journal_entries[0].journal_entry_id
        == sub_entities[0].journal_entry_id
    )
    assert journal_entry.inner_journal_entries[0].amount == sub_entities[0].amount
    assert (
        journal_entry.inner_journal_entries[0].credit_debit
        == sub_entities[0].credit_debit
    )
    assert journal_entry.inner_journal_entries[0].index
    assert journal_entry.inner_journal_entries[0].index == sub_entities[0].index
    assert (
        journal_entry.inner_journal_entries[1].journal_entry_id
        == sub_entities[1].journal_entry_id
    )
    assert journal_entry.inner_journal_entries[1].amount == sub_entities[1].amount
    assert (
        journal_entry.inner_journal_entries[1].credit_debit
        == sub_entities[1].credit_debit
    )
    assert journal_entry.inner_journal_entries[1].index
    assert journal_entry.inner_journal_entries[1].index == sub_entities[1].index

    journal_entry = journal_entries[1]
    entity = entities[1]
    assert journal_entry.id == entity.id
    assert journal_entry.name
    assert journal_entry.name == entity.name
    assert journal_entry.description
    assert journal_entry.description == entity.description
    assert journal_entry.target_date == entity.target_date
    assert journal_entry.status == entity.status

    assert len(journal_entry.inner_journal_entries) == 1
    assert (
        journal_entry.inner_journal_entries[0].journal_entry_id
        == sub_entities[2].journal_entry_id
    )
    assert journal_entry.inner_journal_entries[0].amount == sub_entities[2].amount
    assert (
        journal_entry.inner_journal_entries[0].credit_debit
        == sub_entities[2].credit_debit
    )
    assert journal_entry.inner_journal_entries[0].index
    assert journal_entry.inner_journal_entries[0].index == sub_entities[2].index

    journal_entry = journal_entries[2]
    entity = entities[2]
    assert journal_entry.id == entity.id
    assert journal_entry.name
    assert journal_entry.name == entity.name
    assert journal_entry.description
    assert journal_entry.description == entity.description
    assert journal_entry.target_date == entity.target_date
    assert journal_entry.status == entity.status


def test_get_journal_entries_service_case02(session: SQLSession):
    entities = [
        JournalEntry(
            id="id_1",
            name="name1",
            description="description1",
            target_date=date(2022, 1, 1),
            status=StatusEnum.FIXED,
        ),
        JournalEntry(
            id="id_2",
            name="name2",
            description="description2",
            target_date=date(2022, 1, 1),
            status=StatusEnum.RESOLVED,
        ),
        JournalEntry(
            id="id_3",
            name="name3",
            description="description3",
            target_date=date(2022, 1, 1),
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

    input = JournalEntriesGraphqlInput(account_id="a")
    results = GetJournalEntriesService(session).execute(input)

    journal_entries = [
        GraphqlConvert.type_to_model(JournalEntry, result) for result in results
    ]

    assert len(journal_entries) == 2

    journal_entry = journal_entries[0]
    entity = entities[0]
    assert journal_entry.id == entity.id
    assert journal_entry.name
    assert journal_entry.name == entity.name
    assert journal_entry.description
    assert journal_entry.description == entity.description
    assert journal_entry.target_date == entity.target_date
    assert journal_entry.status == entity.status

    assert len(journal_entry.inner_journal_entries) == 2
    assert (
        journal_entry.inner_journal_entries[0].journal_entry_id
        == sub_entities[0].journal_entry_id
    )
    assert journal_entry.inner_journal_entries[0].amount == sub_entities[0].amount
    assert (
        journal_entry.inner_journal_entries[0].credit_debit
        == sub_entities[0].credit_debit
    )
    assert journal_entry.inner_journal_entries[0].index
    assert journal_entry.inner_journal_entries[0].index == sub_entities[0].index
    assert (
        journal_entry.inner_journal_entries[1].journal_entry_id
        == sub_entities[1].journal_entry_id
    )
    assert journal_entry.inner_journal_entries[1].amount == sub_entities[1].amount
    assert (
        journal_entry.inner_journal_entries[1].credit_debit
        == sub_entities[1].credit_debit
    )
    assert journal_entry.inner_journal_entries[1].index
    assert journal_entry.inner_journal_entries[1].index == sub_entities[1].index

    journal_entry = journal_entries[1]
    entity = entities[1]
    assert journal_entry.id == entity.id
    assert journal_entry.name
    assert journal_entry.name == entity.name
    assert journal_entry.description
    assert journal_entry.description == entity.description
    assert journal_entry.target_date == entity.target_date
    assert journal_entry.status == entity.status

    assert len(journal_entry.inner_journal_entries) == 1
    assert (
        journal_entry.inner_journal_entries[0].journal_entry_id
        == sub_entities[2].journal_entry_id
    )
    assert journal_entry.inner_journal_entries[0].amount == sub_entities[2].amount
    assert (
        journal_entry.inner_journal_entries[0].credit_debit
        == sub_entities[2].credit_debit
    )
    assert journal_entry.inner_journal_entries[0].index
    assert journal_entry.inner_journal_entries[0].index == sub_entities[2].index


def test_get_journal_entries_service_case03(session: SQLSession):
    entities = [
        JournalEntry(
            name="name1",
            description="description1",
            target_date=date(2022, 1, 1),
            status=StatusEnum.FIXED,
        ),
        JournalEntry(
            name="name2",
            description="description2",
            target_date=date(2022, 1, 1),
            status=StatusEnum.RESOLVED,
        ),
        JournalEntry(
            name="name3",
            description="description3",
            target_date=date(2022, 1, 1),
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

    input = JournalEntriesGraphqlInput(account_id="b")
    results = GetJournalEntriesService(session).execute(input)

    journal_entries = [
        GraphqlConvert.type_to_model(JournalEntry, result) for result in results
    ]

    assert len(journal_entries) == 1

    journal_entry = journal_entries[0]
    entity = entities[0]
    assert journal_entry.id == entity.id
    assert journal_entry.name
    assert journal_entry.name == entity.name
    assert journal_entry.description
    assert journal_entry.description == entity.description
    assert journal_entry.target_date == entity.target_date
    assert journal_entry.status == entity.status

    assert len(journal_entry.inner_journal_entries) == 2
    assert (
        journal_entry.inner_journal_entries[0].journal_entry_id
        == sub_entities[0].journal_entry_id
    )
    assert journal_entry.inner_journal_entries[0].amount == sub_entities[0].amount
    assert (
        journal_entry.inner_journal_entries[0].credit_debit
        == sub_entities[0].credit_debit
    )
    assert journal_entry.inner_journal_entries[0].index
    assert journal_entry.inner_journal_entries[0].index == sub_entities[0].index
    assert (
        journal_entry.inner_journal_entries[1].journal_entry_id
        == sub_entities[1].journal_entry_id
    )
    assert journal_entry.inner_journal_entries[1].amount == sub_entities[1].amount
    assert (
        journal_entry.inner_journal_entries[1].credit_debit
        == sub_entities[1].credit_debit
    )
    assert journal_entry.inner_journal_entries[1].index
    assert journal_entry.inner_journal_entries[1].index == sub_entities[1].index
