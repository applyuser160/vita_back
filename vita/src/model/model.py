from datetime import date
from enum import IntEnum

from src.util.sql_model import Base


class DeptEnum(IntEnum):
    pass  # TODO: 内容記載


class BsPlEnum(IntEnum):
    pass  # TODO: 内容記載


class CreditDevitEnum(IntEnum):
    pass  # TODO: 内容記載


class StatusEnum(IntEnum):
    pass  # TODO: 内容記載


class Account(Base, table=True):  # type: ignore
    __tablename__ = "account"
    name: str
    description: str
    dept: DeptEnum
    bs_pl: BsPlEnum
    credit_debit: CreditDevitEnum


class SubAccount(Base, table=True):  # type: ignore
    __tablename__ = "sub_account"
    name: str
    account_id: str
    description: str


class InnerJournalEntry(Base, table=True):  # type: ignore
    __tablename__ = "inner_journal_entry"
    journal_entry_id: str
    account_id: str
    sub_account_id: str
    amount: int
    credit_debit: CreditDevitEnum
    index: int


class JournalEntry(Base, table=True):  # type: ignore
    __tablename__ = "journal_entry"
    date: date
    status: StatusEnum
