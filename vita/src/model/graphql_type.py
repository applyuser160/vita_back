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


@strawberry.experimental.pydantic.type(model=JournalEntry, all_fields=True)
class JournalEntryGraphqlType:
    pass
