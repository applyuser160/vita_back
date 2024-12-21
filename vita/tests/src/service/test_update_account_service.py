from vita.src.model.graphql_input import AccountGraphqlInput
from vita.src.model.model import Account, BsPlEnum, CreditDebitEnum, DeptEnum
from vita.src.service.update_account_service import UpdateAccountService
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
