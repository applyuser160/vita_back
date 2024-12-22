from datetime import datetime
from unittest.mock import Mock, patch
from vita.src.model.graphql_input import AccountGraphqlInput
from vita.src.model.model import Account, BsPlEnum, CreditDebitEnum, DeptEnum
from vita.src.service.delete_account_service import DeleteAccountService
from vita.src.util.sql_model import SQLSession


@patch("util.dt.VitaDatetime.now")
def test_delete_account_service_case01(now: Mock, session: SQLSession):
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

    input = AccountGraphqlInput.from_pydantic(account)

    service = DeleteAccountService(session)
    result = service.execute(input)

    account: Account = result.to_pydantic()

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
    assert account.create_object_id == "system"
    assert account.update_date
    assert account.create_date == datetime(2024, 1, 1, 9, 0, 0, 0)
    assert account.update_object_id
    assert account.update_object_id == "system"
    assert account.delete_date
    assert account.delete_date == datetime(2024, 1, 1, 9, 0, 0, 0)
    assert account.delete_object_id
