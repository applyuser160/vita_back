import strawberry
from model.model import Account, InnerJournalEntry, JournalEntry, SubAccount


@strawberry.experimental.pydantic.type(model=Account, all_fields=True)
class AccountGraphqlType:
    pass


@strawberry.experimental.pydantic.type(model=SubAccount, all_fields=True)
class SubAccountGraphqlType:
    pass


@strawberry.experimental.pydantic.type(model=InnerJournalEntry, all_fields=True)
class InnerJournalEntryGraphqlType:
    pass


@strawberry.experimental.pydantic.type(model=JournalEntry)
class JournalEntryGraphqlType:
    id: strawberry.auto
    name: strawberry.auto
    description: strawberry.auto
    date: strawberry.auto
    status: strawberry.auto
    create_date: strawberry.auto
    create_object_id: strawberry.auto
    update_date: strawberry.auto
    update_object_id: strawberry.auto
    delete_date: strawberry.auto
    delete_object_id: strawberry.auto
    inner_journal_entries: list[InnerJournalEntryGraphqlType]
