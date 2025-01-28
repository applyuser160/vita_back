from datetime import datetime
import json
from unittest.mock import Mock, patch

from sqlmodel import select

from vita.src.model.convert import GraphqlConvert
from vita.src.model.graphql_input import AccountGraphqlInput, SubAccountGraphqlInput
from vita.src.model.graphql_type import AccountGraphqlType, VitaErrorGraphqlType
from vita.src.model.model import (
    Account,
    BsPlEnum,
    CreditDebitEnum,
    DeptEnum,
    SubAccount,
)
from vita.src.service.create_account_service import CreateAccountService
from vita.src.util.constant import SYSTEM_USER
from vita.src.util.dt import VitaDatetime
from vita.src.util.sql_model import SQLSession


def test_a(session: SQLSession):
    input = AccountGraphqlInput(
        name="0" * 101,
        description="des",
        dept=DeptEnum.CURRENT_ASSETS,
        bs_pl=BsPlEnum.BS,
        credit_debit=CreditDebitEnum.DEBIT,
    )
    sub_input = SubAccountGraphqlInput(
        name="name",
        description="desc",
    )

    a: type[Account] = GraphqlConvert.get_model(input=input)
    print(a.__dir__(a()))
    b = a().get_columns_and_relationships()
    print(b)

    d: type[SubAccount] = GraphqlConvert.get_model(input=sub_input)
    e = d().get_columns_and_relationships()
    print(e)

    model = GraphqlConvert.input_to_model(Account, input)
    assert model.name == "0" * 101


def test_create_account_service_case01(session: SQLSession):
    """
    テスト観点:
    バリデーションエラー(勘定科目名が100文字を超過)
    """

    input = AccountGraphqlInput(
        name="0" * 101,
        description="des",
        dept=DeptEnum.CURRENT_ASSETS,
        bs_pl=BsPlEnum.BS,
        credit_debit=CreditDebitEnum.DEBIT,
    )

    service = CreateAccountService(session)
    result = service.execute(input)

    assert isinstance(result, VitaErrorGraphqlType)
    assert result.error_code == 400
    message_dict = json.loads(result.message)[0]
    assert message_dict["title"] == "validation error"
    assert message_dict["type"] == "string_too_long"
    assert message_dict["message"] == "String should have at most 100 characters"
    assert message_dict["location"] == ["name"]


def test_create_account_service_case02(session: SQLSession):
    """
    テスト観点:
    バリデーションエラー(勘定科目名が空)
    """

    input = AccountGraphqlInput(
        name=None,
        description="des",
        dept=DeptEnum.CURRENT_ASSETS,
        bs_pl=BsPlEnum.BS,
        credit_debit=CreditDebitEnum.DEBIT,
    )

    service = CreateAccountService(session)
    result = service.execute(input)

    assert isinstance(result, VitaErrorGraphqlType)
    assert result.error_code == 400
    message_dict = json.loads(result.message)[0]
    assert message_dict["title"] == "validation error"
    assert message_dict["type"] == "string_type"
    assert message_dict["message"] == "Input should be a valid string"
    assert message_dict["location"] == ["name"]


def test_create_account_service_case03(session: SQLSession):
    """
    テスト観点:
    バリデーションエラー(説明が500文字を超過)
    """

    input = AccountGraphqlInput(
        name="name",
        description="0" * 501,
        dept=DeptEnum.CURRENT_ASSETS,
        bs_pl=BsPlEnum.BS,
        credit_debit=CreditDebitEnum.DEBIT,
    )

    service = CreateAccountService(session)
    result = service.execute(input)

    assert isinstance(result, VitaErrorGraphqlType)
    assert result.error_code == 400
    message_dict = json.loads(result.message)[0]
    assert message_dict["title"] == "validation error"
    assert message_dict["type"] == "string_too_long"
    assert message_dict["message"] == "String should have at most 500 characters"
    assert message_dict["location"] == ["description"]


def test_create_account_service_case04(session: SQLSession):
    """
    テスト観点:
    最大長入力(勘定科目名、説明)
    バリデーションエラー(分類が空)
    """

    input = AccountGraphqlInput(
        name="0" * 100,
        description="0" * 500,
        dept=None,
        bs_pl=None,
        credit_debit=None,
    )

    service = CreateAccountService(session)
    result = service.execute(input)

    assert isinstance(result, VitaErrorGraphqlType)
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
def test_create_account_service_case05(now: Mock, session: SQLSession):
    """
    テスト観点:
    正常系
    """

    now.return_value = datetime(2024, 1, 1, 9, 0, 0, 0)

    input = AccountGraphqlInput(
        name="name",
        description="des",
        dept=DeptEnum.CURRENT_ASSETS,
        bs_pl=BsPlEnum.BS,
        credit_debit=CreditDebitEnum.DEBIT,
    )

    service = CreateAccountService(session)
    result: AccountGraphqlType = service.execute(input)
    account: Account = GraphqlConvert.type_to_model(Account, result)

    print(result)
    print(account)

    assert account.id
    assert account.name == "name"
    assert account.description
    assert account.description == "des"
    assert account.dept == DeptEnum.CURRENT_ASSETS
    assert account.bs_pl == BsPlEnum.BS
    assert account.credit_debit == CreditDebitEnum.DEBIT
    assert account.create_date
    assert account.create_date == datetime(2024, 1, 1, 9, 0, 0, 0)
    assert account.create_object_id
    assert account.create_object_id == SYSTEM_USER
    assert account.update_date
    assert account.create_date == datetime(2024, 1, 1, 9, 0, 0, 0)
    assert account.update_object_id
    assert account.update_object_id == SYSTEM_USER
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
