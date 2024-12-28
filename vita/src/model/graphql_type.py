from typing import TypeVar
import strawberry
from vita.src.model.model import Account, InnerJournalEntry, JournalEntry, SubAccount


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


Y = TypeVar(
    "Y",
    AccountGraphqlType,
    SubAccountGraphqlType,
    JournalEntryGraphqlType,
    InnerJournalEntryGraphqlType,
)


TypeUnion = (
    AccountGraphqlType
    | SubAccountGraphqlType
    | JournalEntryGraphqlType
    | InnerJournalEntryGraphqlType
)
