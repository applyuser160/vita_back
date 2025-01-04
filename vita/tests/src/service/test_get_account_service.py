from vita.src.model.graphql_input import SingleGraphqlInput
from vita.src.model.model import (
    Account,
    BsPlEnum,
    CreditDebitEnum,
    DeptEnum,
    SubAccount,
)
from vita.src.service.get_account_service import GetAccountService
from vita.src.util.constant import SYSTEM_USER
from vita.src.util.sql_model import SQLSession
from vita.src.model.convert import GraphqlConvert


def test_get_account_service_case01(session: SQLSession):
    entity = Account(
        name="name",
        description="des",
        dept=DeptEnum.CURRENT_ASSETS,
        bs_pl=BsPlEnum.BS,
        credit_debit=CreditDebitEnum.DEBIT,
    )
    entity = session.save(Account, entity, SYSTEM_USER)

    sub_entity = SubAccount(
        name="name",
        account_id=entity.id,
        description="desc",
    )
    sub_entity = session.save(SubAccount, sub_entity, SYSTEM_USER)

    input = SingleGraphqlInput(id=entity.id)
    result = GetAccountService(session).execute(input)

    account = GraphqlConvert.type_to_model(Account, result)

    assert entity
    assert account.name == entity.name
    assert account.description == entity.description
    assert account.dept == entity.dept
    assert account.bs_pl == entity.bs_pl
    assert account.credit_debit == entity.credit_debit
    assert len(account.sub_accounts) == 1
    assert account.sub_accounts[0].name == sub_entity.name
    assert account.sub_accounts[0].description == sub_entity.description
