from datetime import datetime
from unittest.mock import Mock, patch

from sqlmodel import select
from vita.src.model.graphql_input import SubAccountGraphqlInput
from vita.src.model.graphql_type import SubAccountGraphqlType
from vita.src.model.model import SubAccount
from vita.src.service.delete_sub_account_service import DeleteSubAccountService
from vita.src.util.dt import VitaDatetime
from vita.src.util.sql_model import SQLSession


@patch.object(VitaDatetime, "now")
def test_update_account_service_case01(now: Mock, session: SQLSession):
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
    sub_account = session.save(SubAccount, sub_account, "system")

    input = SubAccountGraphqlInput.from_pydantic(sub_account)

    service = DeleteSubAccountService(session)
    result: SubAccountGraphqlType = service.execute(input)
    sub_account: SubAccount = result.to_pydantic()

    assert sub_account.id
    assert sub_account.name == "name"
    assert sub_account.account_id == "id"
    assert sub_account.description
    assert sub_account.description == "des"
    assert sub_account.update_date
    assert sub_account.update_date == datetime(2024, 1, 1, 9, 0, 0, 0)
    assert sub_account.update_object_id
    assert sub_account.update_object_id == "system"
    assert sub_account.update_date
    assert sub_account.update_date == datetime(2024, 1, 1, 9, 0, 0, 0)
    assert sub_account.update_object_id
    assert sub_account.update_object_id == "system"
    assert sub_account.delete_date
    assert sub_account.delete_date == datetime(2024, 1, 1, 9, 0, 0, 0)
    assert sub_account.delete_object_id

    record = session.execute(
        select(SubAccount).where(SubAccount.id == sub_account.id), SubAccount, True
    )
    assert record
    assert sub_account.id == record.id
    assert sub_account.name == record.name
    assert sub_account.description == record.description
    assert sub_account.create_date == record.create_date
    assert sub_account.create_object_id == record.create_object_id
    assert sub_account.update_date == record.update_date
    assert sub_account.update_object_id == record.update_object_id
    assert sub_account.delete_date == record.delete_date
    assert sub_account.delete_object_id == record.delete_object_id
