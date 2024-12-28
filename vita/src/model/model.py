from datetime import date
from enum import IntEnum

import strawberry
from sqlmodel import Field, Relationship
from vita.src.util.sql_model import Base


@strawberry.enum
class DeptEnum(IntEnum):
    CURRENT_ASSETS = 1
    """
    流動資産
    """
    SALES_CLAIM = 2
    """
    売上債権
    """
    INVENTORY = 3
    """
    棚卸資産
    """
    OTHER_CURRENT_ASSETS = 4
    """
    他流動資産
    """
    PROPERTY_PLANT_AND_EQUIPMENT = 5
    """
    有形固定資産
    """
    INTANGIBLE_ASSETS = 6
    """
    無形固定資産
    """
    DEFERRED_ASSETS = 7
    """
    繰延資産
    """
    PURCHASE_DEBT = 8
    """
    仕入債務
    """
    OTHER_CURRENT_LIABILITIES = 9
    """
    他流動負債
    """
    FIXED_LIABILITY = 10
    """
    固定負債
    """
    SALES = 11
    """
    売上高
    """
    SALES_MANAGEMENT_EXPENSES = 12
    """
    販売管理費
    """
    NON_OPERATING_INCOME = 13
    """
    営業外収益
    """
    NON_OPERATING_EXPENSES = 14
    """
    営業外費用
    """
    EXTRA_ORDINARY_GAINS = 15
    """
    特別利益
    """
    EXTRAORDINARY_LOSSES = 16
    """
    特別損失
    """


@strawberry.enum
class BsPlEnum(IntEnum):
    BS = 1
    """
    貸借対照表
    """
    PL = 2
    """
    損益計算書
    """


@strawberry.enum
class CreditDebitEnum(IntEnum):
    CREDIT = 1
    """
    貸方
    """
    DEBIT = 2
    """
    借方
    """


@strawberry.enum
class StatusEnum(IntEnum):
    UNFIXED = 1
    """
    未確定
    """
    FIXED = 2
    """
    確定済み
    """
    RESOLVED = 3
    """
    解決済み
    """


class Account(Base, table=True):  # type: ignore
    __tablename__ = "account"
    name: str = Field(max_length=100)
    description: str | None = Field(default=None, max_length=500)
    dept: DeptEnum
    bs_pl: BsPlEnum
    credit_debit: CreditDebitEnum

    sub_accounts: list["SubAccount"] = Relationship(back_populates="account")
    inner_journal_entries_account: list["InnerJournalEntry"] = Relationship(
        back_populates="account"
    )


class SubAccount(Base, table=True):  # type: ignore
    __tablename__ = "sub_account"
    name: str = Field(max_length=100)
    account_id: str = Field(foreign_key="account.id", max_length=40)
    description: str | None = Field(default=None, max_length=500)

    account: Account | None = Relationship(back_populates="sub_accounts")
    inner_journal_entries_sub: list["InnerJournalEntry"] = Relationship(
        back_populates="sub_account"
    )


class JournalEntry(Base, table=True):  # type: ignore
    __tablename__ = "journal_entry"
    name: str | None = Field(default=None, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    date: date
    status: StatusEnum
    inner_journal_entries: list["InnerJournalEntry"] = Relationship(
        back_populates="journal_entry"
    )


class InnerJournalEntry(Base, table=True):  # type: ignore
    __tablename__ = "inner_journal_entry"
    journal_entry_id: str = Field(foreign_key="journal_entry.id", max_length=40)
    account_id: str = Field(foreign_key="account.id", max_length=40)
    sub_account_id: str = Field(foreign_key="sub_account.id", max_length=40)
    amount: int
    credit_debit: CreditDebitEnum
    index: int | None = Field(default=None)

    account: Account | None = Relationship(
        back_populates="inner_journal_entries_account"
    )
    sub_account: SubAccount | None = Relationship(
        back_populates="inner_journal_entries_sub"
    )
    journal_entry: JournalEntry | None = Relationship(
        back_populates="inner_journal_entries"
    )


ModelUnion = Account | SubAccount | JournalEntry | InnerJournalEntry
