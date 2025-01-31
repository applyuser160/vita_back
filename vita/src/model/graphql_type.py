from datetime import datetime, date
from typing import TypeVar, ForwardRef
import strawberry
from vita.src.model.model import (
    BsPlEnum,
    CreditDebitEnum,
    DeptEnum,
    StatusEnum,
)


@strawberry.type
class BaseGraphqlType:
    id: str | None = None
    create_date: datetime | None = None
    create_object_id: str | None = None
    update_date: datetime | None = None
    update_object_id: str | None = None
    delete_date: datetime | None = None
    delete_object_id: str | None = None


@strawberry.type
class AccountGraphqlType(BaseGraphqlType):
    name: str | None = None
    description: str | None = None
    dept: DeptEnum | None = None
    bs_pl: BsPlEnum | None = None
    credit_debit: CreditDebitEnum | None = None
    sub_accounts: list["SubAccountGraphqlType"] | None = None


@strawberry.type
class SubAccountGraphqlType(BaseGraphqlType):
    name: str | None = None
    account_id: str | None = None
    description: str | None = None
    account: AccountGraphqlType | None = None


@strawberry.type
class InnerJournalEntryGraphqlType(BaseGraphqlType):
    journal_entry_id: str | None = None
    account_id: str | None = None
    sub_account_id: str | None = None
    amount: int | None = None
    credit_debit: CreditDebitEnum | None = None
    index: int | None = None
    account: AccountGraphqlType | None = None
    sub_account: SubAccountGraphqlType | None = None
    journal_entry: ForwardRef("JournalEntryGraphqlType") | None = None  # type: ignore


@strawberry.type
class JournalEntryGraphqlType(BaseGraphqlType):
    name: str | None = None
    description: str | None = None
    target_date: date | None = None
    status: StatusEnum | None = None
    inner_journal_entries: list[InnerJournalEntryGraphqlType] | None = None


@strawberry.type
class BalanceGraphqlType(BaseGraphqlType):
    account_id: str | None = None
    sub_account_id: str | None = None
    total_amount: int | None = None


@strawberry.type
class DailyBalanceGraphqlType(BaseGraphqlType):
    account_id: str | None = None
    sub_account_id: str | None = None
    target_date: date | None = None
    total_amount: int | None = None


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
