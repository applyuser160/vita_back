from datetime import datetime
from unittest.mock import Mock, patch

from sqlmodel import select
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
    account = session.save(Account, account, "system")

    input = AccountGraphqlInput.from_pydantic(account)

    service = DeleteAccountService(session)
    result = service.execute(input)

    account = result.to_pydantic()

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

    record: Account = session.execute(
        select(Account).where(Account.id == account.id), Account, True
    )
    assert record
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
