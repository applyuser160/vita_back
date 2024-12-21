from datetime import date

import pydantic
import strawberry
from model.model import (
    Account,
    BsPlEnum,
    CreditDebitEnum,
    DeptEnum,
    InnerJournalEntry,
    JournalEntry,
    StatusEnum,
    SubAccount,
)
from strawberry.experimental.pydantic.conversion_types import StrawberryTypeFromPydantic


@strawberry.experimental.pydantic.input(model=Account, all_fields=True)
class AccountGraphqlInput(StrawberryTypeFromPydantic):
    pass


@strawberry.experimental.pydantic.input(model=SubAccount, all_fields=True)
class SubAccountGraphqlInput:
    pass


@strawberry.experimental.pydantic.input(model=InnerJournalEntry, all_fields=True)
class InnerJournalEntryGraphqlInput:
    pass


@strawberry.experimental.pydantic.input(model=JournalEntry)
class JournalEntryGraphqlInput:
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
    inner_journal_entries: list[InnerJournalEntryGraphqlInput]


@strawberry.input
class SingleGraphqlInput:
    id: str


@strawberry.input
class AccountsGraphqlInput:
    name: str | None
    description: str | None
    dept: DeptEnum | None
    bs_pl: BsPlEnum | None
    credit_debit: CreditDebitEnum | None


@strawberry.input
class SubAccountsGraphqlInput:
    name: str | None
    account_id: str | None
    description: str | None


@strawberry.input
class JournalEntriesGraphqlInput:
    name: str | None
    description: str | None
    from_date: date | None
    to_date: date | None
    status: StatusEnum | None
    account_id: str | None
    sub_account_id: str | None
