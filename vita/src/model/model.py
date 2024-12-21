from datetime import date
from enum import IntEnum

from src.util.sql_model import Base


class DeptEnum(IntEnum):
    pass  # TODO: 内容記載


class BsPlEnum(IntEnum):
    pass  # TODO: 内容記載


class CreditDebitEnum(IntEnum):
    pass  # TODO: 内容記載


class StatusEnum(IntEnum):
    pass  # TODO: 内容記載


class Account(Base, table=True):  # type: ignore
    __tablename__ = "account"
    name: str
    description: str | None
    dept: DeptEnum
    bs_pl: BsPlEnum
    credit_debit: CreditDebitEnum


class SubAccount(Base, table=True):  # type: ignore
    __tablename__ = "sub_account"
    name: str
    account_id: str
    description: str | None


class InnerJournalEntry(Base, table=True):  # type: ignore
    __tablename__ = "inner_journal_entry"
    journal_entry_id: str
    account_id: str
    sub_account_id: str
    amount: int
    credit_debit: CreditDebitEnum
    index: int | None


class JournalEntry(Base, table=True):  # type: ignore
    __tablename__ = "journal_entry"
    name: str | None
    description: str | None
    date: date
    status: StatusEnum
