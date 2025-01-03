from datetime import date
from typing import TypeVar

import strawberry
from vita.src.model.model import (
    Account,
    BsPlEnum,
    CreditDebitEnum,
    DeptEnum,
    InnerJournalEntry,
    JournalEntry,
    StatusEnum,
    SubAccount,
)


@strawberry.experimental.pydantic.input(model=Account, all_fields=True)
class AccountGraphqlInput:
    pass


@strawberry.experimental.pydantic.input(model=SubAccount, all_fields=True)
class SubAccountGraphqlInput:
    pass


@strawberry.experimental.pydantic.input(model=InnerJournalEntry, all_fields=True)
class InnerJournalEntryGraphqlInput:
    pass


@strawberry.experimental.pydantic.input(model=JournalEntry, all_fields=True)
class JournalEntryGraphqlInput:
    pass


@strawberry.input
class SingleGraphqlInput:
    id: str


@strawberry.input
class AccountsGraphqlInput:
    name: str | None = None
    description: str | None = None
    dept: DeptEnum | None = None
    bs_pl: BsPlEnum | None = None
    credit_debit: CreditDebitEnum | None = None


@strawberry.input
class SubAccountsGraphqlInput:
    name: str | None = None
    account_id: str | None = None
    description: str | None = None


@strawberry.input
class JournalEntriesGraphqlInput:
    name: str | None = None
    description: str | None = None
    from_date: date | None = None
    to_date: date | None = None
    status: StatusEnum | None = None
    account_id: str | None = None
    sub_account_id: str | None = None


I = TypeVar(
    "I",
    AccountGraphqlInput,
    SubAccountGraphqlInput,
    JournalEntryGraphqlInput,
    InnerJournalEntryGraphqlInput,
)


InputUnion = (
    AccountGraphqlInput
    | SubAccountGraphqlInput
    | JournalEntryGraphqlInput
    | InnerJournalEntryGraphqlInput
)
