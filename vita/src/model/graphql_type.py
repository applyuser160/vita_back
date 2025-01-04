from typing import TypeVar
import strawberry
from vita.src.model.model import (
    Account,
    Balance,
    DailyBalance,
    InnerJournalEntry,
    JournalEntry,
    SubAccount,
)


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


@strawberry.experimental.pydantic.type(model=Balance, all_fields=True)
class BalanceGraphqlType:
    pass


@strawberry.experimental.pydantic.type(model=DailyBalance, all_fields=True)
class DailyBalanceGraphqlType:
    pass


Y = TypeVar(
    "Y",
    AccountGraphqlType,
    SubAccountGraphqlType,
    JournalEntryGraphqlType,
    InnerJournalEntryGraphqlType,
    BalanceGraphqlType,
    DailyBalanceGraphqlType,
)


TypeUnion = (
    AccountGraphqlType
    | SubAccountGraphqlType
    | JournalEntryGraphqlType
    | InnerJournalEntryGraphqlType
    | BalanceGraphqlType
    | DailyBalanceGraphqlType
)
