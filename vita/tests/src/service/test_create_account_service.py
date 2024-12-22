import json
from vita.src.model.graphql_input import AccountGraphqlInput
from vita.src.model.model import Account, BsPlEnum, CreditDebitEnum, DeptEnum
from vita.src.service.create_account_service import CreateAccountService
from vita.src.util.sql_model import SQLSession


def test_create_account_service_case01(session: SQLSession):
    """
    テスト観点:
    バリデーションエラー(勘定科目名が100文字を超過)
    """

    account = Account(
        name="0" * 101,
        description="des",
        dept=DeptEnum.CURRENT_ASSETS,
        bs_pl=BsPlEnum.BS,
        credit_debit=CreditDebitEnum.DEBIT,
    )
    input = AccountGraphqlInput.from_pydantic(account)

    service = CreateAccountService(session)
    result = service.execute(input)

    assert issubclass(type(result), Exception)
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

    account = Account(
        name=None,
        description="des",
        dept=DeptEnum.CURRENT_ASSETS,
        bs_pl=BsPlEnum.BS,
        credit_debit=CreditDebitEnum.DEBIT,
    )
    input = AccountGraphqlInput.from_pydantic(account)

    service = CreateAccountService(session)
    result = service.execute(input)

    assert issubclass(type(result), Exception)
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

    account = Account(
        name="name",
        description="0" * 501,
        dept=DeptEnum.CURRENT_ASSETS,
        bs_pl=BsPlEnum.BS,
        credit_debit=CreditDebitEnum.DEBIT,
    )
    input = AccountGraphqlInput.from_pydantic(account)

    service = CreateAccountService(session)
    result = service.execute(input)

    assert issubclass(type(result), Exception)
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

    account = Account(
        name="0" * 100,
        description="0" * 500,
        dept=None,
        bs_pl=None,
        credit_debit=None,
    )
    input = AccountGraphqlInput.from_pydantic(account)

    service = CreateAccountService(session)
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
