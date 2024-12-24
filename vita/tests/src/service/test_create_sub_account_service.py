from datetime import datetime
import json
from unittest.mock import Mock, patch
from vita.src.model.graphql_input import SubAccountGraphqlInput
from vita.src.model.graphql_type import SubAccountGraphqlType
from vita.src.model.model import SubAccount
from vita.src.service.create_sub_account_service import CreateSubAccountService
from vita.src.util.sql_model import SQLSession


def test_create_sub_account_service_case01(session: SQLSession):
    """
    テスト観点:
    バリデーションエラー(勘定科目名が100文字を超過)
    """

    sub_account = SubAccount(
        name="0" * 101,
        account_id="id",
        description="des",
    )
    input = SubAccountGraphqlInput.from_pydantic(sub_account)

    service = CreateSubAccountService(session)
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

    sub_account = SubAccount(
        name=None,
        account_id="id",
        description="des",
    )
    input = SubAccountGraphqlInput.from_pydantic(sub_account)

    service = CreateSubAccountService(session)
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

    sub_account = SubAccount(
        name="name",
        account_id="id",
        description="0" * 501,
    )
    input = SubAccountGraphqlInput.from_pydantic(sub_account)

    service = CreateSubAccountService(session)
    result = service.execute(input)

    assert issubclass(type(result), Exception)
    assert result.error_code == 400
    message_dict = json.loads(result.message)[0]
    assert message_dict["title"] == "validation error"
    assert message_dict["type"] == "string_too_long"
    assert message_dict["message"] == "String should have at most 500 characters"
    assert message_dict["location"] == ["description"]


@patch("util.dt.VitaDatetime.now")
def test_create_account_service_case05(now: Mock, session: SQLSession):
    """
    テスト観点:
    正常系
    """

    now.return_value = datetime(2024, 1, 1, 9, 0, 0, 0)

    sub_account = SubAccount(
        name="name",
        account_id="id",
        description="des",
    )
    input = SubAccountGraphqlInput.from_pydantic(sub_account)

    service = CreateSubAccountService(session)
    result: SubAccountGraphqlType = service.execute(input)
    sub_account: SubAccount = result.to_pydantic()

    assert sub_account.id
    assert sub_account.name == "name"
    assert sub_account.account_id == "id"
    assert sub_account.description
    assert sub_account.description == "des"
    assert sub_account.create_date
    assert sub_account.create_date == datetime(2024, 1, 1, 9, 0, 0, 0)
    assert sub_account.create_object_id
    assert sub_account.create_object_id == "system"
    assert sub_account.update_date
    assert sub_account.create_date == datetime(2024, 1, 1, 9, 0, 0, 0)
    assert sub_account.update_object_id
    assert sub_account.update_object_id == "system"
    assert not sub_account.delete_date
    assert not sub_account.delete_object_id
