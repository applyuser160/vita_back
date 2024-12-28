from datetime import datetime
import json
from unittest.mock import Mock, patch

from sqlmodel import select
from vita.src.model.graphql_input import AccountGraphqlInput
from vita.src.model.model import Account, BsPlEnum, CreditDebitEnum, DeptEnum
from vita.src.service.update_account_service import UpdateAccountService
from vita.src.util.dt import VitaDatetime
from vita.src.util.sql_model import SQLSession


def test_update_account_service_case01(session: SQLSession):
    """
    テスト観点:
    バリデーションエラー(勘定科目名が100文字を超過)
    """

    account = Account(
        name="0" * 100,
        description="des",
        dept=DeptEnum.CURRENT_ASSETS,
        bs_pl=BsPlEnum.BS,
        credit_debit=CreditDebitEnum.DEBIT,
    )
    account: Account = session.save(Account, account, "system")

    account.name = "0" * 101
    input = AccountGraphqlInput.from_pydantic(account)

    service = UpdateAccountService(session)
    result = service.execute(input)

    assert issubclass(type(result), Exception)
    assert result.error_code == 400


def test_update_account_service_case02(session: SQLSession):
    """
    テスト観点:
    バリデーションエラー(勘定科目名が空)
    """

    account = Account(
        name="name",
        description="des",
        dept=DeptEnum.CURRENT_ASSETS,
        bs_pl=BsPlEnum.BS,
        credit_debit=CreditDebitEnum.DEBIT,
    )
    account: Account = session.save(Account, account, "system")

    account.name = None
    input = AccountGraphqlInput.from_pydantic(account)

    service = UpdateAccountService(session)
    result = service.execute(input)

    assert issubclass(type(result), Exception)
    assert result.error_code == 400
    message_dict = json.loads(result.message)[0]
    assert message_dict["title"] == "validation error"
    assert message_dict["type"] == "string_type"
    assert message_dict["message"] == "Input should be a valid string"
    assert message_dict["location"] == ["name"]


def test_update_account_service_case03(session: SQLSession):
    """
    テスト観点:
    バリデーションエラー(説明が500文字を超過)
    """

    account = Account(
        name="name",
        description="des",
        dept=DeptEnum.CURRENT_ASSETS,
        bs_pl=BsPlEnum.BS,
        credit_debit=CreditDebitEnum.DEBIT,
    )
    account: Account = session.save(Account, account, "system")

    account.description = "0" * 501
    input = AccountGraphqlInput.from_pydantic(account)

    service = UpdateAccountService(session)
    result = service.execute(input)

    assert issubclass(type(result), Exception)
    assert result.error_code == 400
    message_dict = json.loads(result.message)[0]
    assert message_dict["title"] == "validation error"
    assert message_dict["type"] == "string_too_long"
    assert message_dict["message"] == "String should have at most 500 characters"
    assert message_dict["location"] == ["description"]


def test_update_account_service_case04(session: SQLSession):
    """
    テスト観点:
    最大長入力(勘定科目名、説明)
    バリデーションエラー(分類が空)
    """

    account = Account(
        name="0" * 100,
        description="0" * 500,
        dept=DeptEnum.CURRENT_ASSETS,
        bs_pl=BsPlEnum.BS,
        credit_debit=CreditDebitEnum.DEBIT,
    )
    account: Account = session.save(Account, account, "system")

    account.dept = None
    account.bs_pl = None
    account.credit_debit = None
    input = AccountGraphqlInput.from_pydantic(account)

    service = UpdateAccountService(session)
    result = service.execute(input)

    assert issubclass(type(result), Exception)
    assert result.error_code == 400

    message_dict = json.loads(result.message)[0]
    assert message_dict["title"] == "validation error"
    assert message_dict["type"] == "enum"
    assert (
        message_dict["message"]
        == "Input should be 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 or 16"
    )
    assert message_dict["location"] == ["dept"]

    message_dict = json.loads(result.message)[1]
    assert message_dict["title"] == "validation error"
    assert message_dict["type"] == "enum"
    assert message_dict["message"] == "Input should be 1 or 2"
    assert message_dict["location"] == ["bs_pl"]

    message_dict = json.loads(result.message)[2]
    assert message_dict["title"] == "validation error"
    assert message_dict["type"] == "enum"
    assert message_dict["message"] == "Input should be 1 or 2"
    assert message_dict["location"] == ["credit_debit"]


@patch.object(VitaDatetime, "now")
def test_update_account_service_case05(now: Mock, session: SQLSession):
    """
    テスト観点:
    正常系
    """

    now.return_value = datetime(2024, 1, 1, 9, 0, 0, 0)

    account = Account(
        name="name",
        description="des",
        dept=DeptEnum.CURRENT_ASSETS,
        bs_pl=BsPlEnum.BS,
        credit_debit=CreditDebitEnum.DEBIT,
    )
    account: Account = session.save(Account, account, "system")

    account.name = "new name"
    account.description = "new description"
    account.dept = DeptEnum.DEFERRED_ASSETS
    account.bs_pl = BsPlEnum.PL
    account.credit_debit = CreditDebitEnum.CREDIT
    input = AccountGraphqlInput.from_pydantic(account)

    service = UpdateAccountService(session)
    result = service.execute(input)
    account: Account = result.to_pydantic()

    assert account.id
    assert account.name == "new name"
    assert account.description
    assert account.description == "new description"
    assert account.dept == DeptEnum.DEFERRED_ASSETS
    assert account.bs_pl == BsPlEnum.PL
    assert account.credit_debit == CreditDebitEnum.CREDIT
    assert account.create_date
    assert account.create_date == datetime(2024, 1, 1, 9, 0, 0, 0)
    assert account.create_object_id
    assert account.create_object_id == "system"
    assert account.update_date
    assert account.create_date == datetime(2024, 1, 1, 9, 0, 0, 0)
    assert account.update_object_id
    assert account.update_object_id == "system"
    assert not account.delete_date
    assert not account.delete_object_id

    record = session.execute(
        select(Account).where(Account.id == account.id), Account, True
    )
    assert record
    assert isinstance(record, Account)
    assert account.id == record.id
    assert account.name == record.name
    assert account.description == record.description
    assert account.dept == record.dept
    assert account.bs_pl == record.bs_pl
    assert account.credit_debit == record.credit_debit
    assert account.create_date == record.create_date
    assert account.create_object_id == record.create_object_id
    assert account.update_date == record.update_date
    assert account.update_object_id == record.update_object_id
    assert account.delete_date == record.delete_date
    assert account.delete_object_id == record.delete_object_id
