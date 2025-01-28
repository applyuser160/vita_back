from datetime import date, datetime
from typing import TypeVar, ForwardRef

import strawberry
from vita.src.model.model import (
    BsPlEnum,
    CreditDebitEnum,
    DeptEnum,
    StatusEnum,
)


@strawberry.input
class BaseGraphqlInput:
    id: str | None = None
    create_date: datetime | None = None
    create_object_id: str | None = None
    update_date: datetime | None = None
    update_object_id: str | None = None
    delete_date: datetime | None = None
    delete_object_id: str | None = None


@strawberry.input
class AccountGraphqlInput(BaseGraphqlInput):
    name: str | None = None
    description: str | None = None
    dept: DeptEnum | None = None
    bs_pl: BsPlEnum | None = None
    credit_debit: CreditDebitEnum | None = None
    sub_accounts: list["SubAccountGraphqlInput"] | None = None


@strawberry.input
class SubAccountGraphqlInput(BaseGraphqlInput):
    name: str | None = None
    account_id: str | None = None
    description: str | None = None
    account: AccountGraphqlInput | None = None


@strawberry.input
class InnerJournalEntryGraphqlInput(BaseGraphqlInput):
    journal_entry_id: str | None = None
    account_id: str | None = None
    sub_account_id: str | None = None
    amount: int | None = None
    credit_debit: CreditDebitEnum | None = None
    index: int | None = None
    account: AccountGraphqlInput | None = None
    sub_account: SubAccountGraphqlInput | None = None
    journal_entry: ForwardRef("JournalEntryGraphqlInput") | None = None  # type: ignore
    # journal_entry: Optional["JournalEntryGraphqlInput"] = None


@strawberry.input
class JournalEntryGraphqlInput(BaseGraphqlInput):
    name: str | None = None
    description: str | None = None
    target_date: date | None = None
    status: StatusEnum | None = None
    inner_journal_entries: list[InnerJournalEntryGraphqlInput] | None = None


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


@strawberry.input
class CollectJournalEntriesGraphqlInput:
    account_ids: list[str] | None = None
    sub_account_ids: list[str] | None = None
    from_date: date | None = None
    to_date: date | None = None


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
