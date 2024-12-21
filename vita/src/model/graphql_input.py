import strawberry
from model.model import Account, InnerJournalEntry, JournalEntry, SubAccount


@strawberry.experimental.pydantic.input(model=Account, all_fields=True)
class AccountGraphqlInput:
    pass


@strawberry.experimental.pydantic.input(model=SubAccount, all_fields=True)
class SubAccountGraphqlType:
    pass


@strawberry.experimental.pydantic.input(model=InnerJournalEntry, all_fields=True)
class InnerJournalEntryGraphqlType:
    pass


@strawberry.experimental.pydantic.input(model=JournalEntry, all_fields=True)
class JournalEntryGraphqlType:
    pass
