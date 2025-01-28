from datetime import datetime


from vita.src.model.graphql_input import (
    InnerJournalEntryGraphqlInput,
    JournalEntryGraphqlInput,
)
from vita.src.model.graphql_type import JournalEntryGraphqlType
from vita.src.model.model import (
    CreditDebitEnum,
    JournalEntry,
    InnerJournalEntry,
    StatusEnum,
)
from vita.src.service.delete_journal_entry_serivce import DeleteJournalEntryService
from vita.src.util.constant import SYSTEM_USER
from vita.src.util.sql_model import SQLSession
from vita.src.model.convert import GraphqlConvert


def test_delete_journal_entry_service_case01(session: SQLSession):
    """
    テスト観点:
    バリデーションエラー()
    """

    inner_journal_entry = InnerJournalEntry(
        id="1",
        journal_entry_id="2",
        account_id="account_id",
        sub_account_id="sub_account_id",
        amount=100,
        credit_debit=CreditDebitEnum.DEBIT,
        index=1,
    )

    journal_entry = JournalEntry(
        id="2",
        name="Sample Journal Entry",
        description="This is a sample journal entry.",
        target_date=datetime.now().date(),
        status=StatusEnum.UNFIXED,
        create_date=datetime.now(),
        create_object_id=SYSTEM_USER,
        update_date=datetime.now(),
        update_object_id=SYSTEM_USER,
        delete_date=None,
        delete_object_id=None,
    )

    session.save(JournalEntry, journal_entry, SYSTEM_USER)
    session.save(InnerJournalEntry, inner_journal_entry, SYSTEM_USER)
    session.session.expire_all()

    inner_input = InnerJournalEntryGraphqlInput(
        id="1",
        journal_entry_id="2",
        account_id="account_id",
        sub_account_id="sub_account_id",
        amount=1000,
        credit_debit=CreditDebitEnum.DEBIT,
        index=1,
    )

    input = JournalEntryGraphqlInput(
        id="2",
        name="update name",
        description="This is a sample journal entry.",
        target_date=datetime.now().date(),
        status=StatusEnum.UNFIXED,
        create_date=datetime.now(),
        create_object_id=SYSTEM_USER,
        update_date=datetime.now(),
        update_object_id=SYSTEM_USER,
        delete_date=None,
        delete_object_id=None,
        inner_journal_entries=[inner_input],
    )

    service = DeleteJournalEntryService(session)
    result: JournalEntryGraphqlType = service.execute(input)

    journal_entry = GraphqlConvert.type_to_model(JournalEntry, result)

    records = session.find(JournalEntry, isOne=False)

    assert isinstance(journal_entry, JournalEntry)
    assert len(journal_entry.inner_journal_entries) == 1
    assert len(records) == 1
    assert len(records[0].inner_journal_entries) == 1
    assert not records[0].inner_journal_entries[0].is_empty()
