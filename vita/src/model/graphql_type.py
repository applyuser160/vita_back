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


@strawberry.experimental.pydantic.type(model=Account)
class AccountGraphqlType:
    id: strawberry.auto
    create_date: strawberry.auto
    create_object_id: strawberry.auto
    update_date: strawberry.auto
    update_object_id: strawberry.auto
    delete_date: strawberry.auto
    delete_object_id: strawberry.auto
    name: strawberry.auto
    description: strawberry.auto
    dept: strawberry.auto
    bs_pl: strawberry.auto
    credit_debit: strawberry.auto
    sub_accounts: list["SubAccountGraphqlType"]


@strawberry.experimental.pydantic.type(model=SubAccount)
class SubAccountGraphqlType:
    id: strawberry.auto
    create_date: strawberry.auto
    create_object_id: strawberry.auto
    update_date: strawberry.auto
    update_object_id: strawberry.auto
    delete_date: strawberry.auto
    delete_object_id: strawberry.auto
    name: strawberry.auto
    account_id: strawberry.auto
    description: strawberry.auto
    account: AccountGraphqlType


@strawberry.experimental.pydantic.type(model=InnerJournalEntry, all_fields=True)
class InnerJournalEntryGraphqlType:
    pass


@strawberry.experimental.pydantic.type(model=JournalEntry)
class JournalEntryGraphqlType:
    id: strawberry.auto
    create_date: strawberry.auto
    create_object_id: strawberry.auto
    update_date: strawberry.auto
    update_object_id: strawberry.auto
    delete_date: strawberry.auto
    delete_object_id: strawberry.auto
    name: strawberry.auto
    description: strawberry.auto
    date: strawberry.auto
    status: strawberry.auto
    inner_journal_entries: list[InnerJournalEntryGraphqlType]


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


@strawberry.type
class VitaErrorGraphqlType:
    error_code: int
    message: str
