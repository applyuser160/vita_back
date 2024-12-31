from vita.src.model.graphql_input import SingleGraphqlInput
from vita.src.model.model import (
    Account,
    BsPlEnum,
    CreditDebitEnum,
    DeptEnum,
    SubAccount,
)
from vita.src.service.get_sub_account_service import GetSubAccountService
from vita.src.util.constant import SYSTEM_USER
from vita.src.util.sql_model import SQLSession
from vita.src.model.convert import GraphqlConvert


def test_get_sub_account_service_case01(session: SQLSession):
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

    input = SingleGraphqlInput(id=sub_entity.id)
    result = GetSubAccountService(session).execute(input)

    sub_account = GraphqlConvert.type_to_model(SubAccount, result)

    assert entity
    assert sub_account.name == sub_entity.name
    assert sub_account.description == sub_entity.description
    assert sub_account.account
    assert sub_account.account.name == entity.name
    assert sub_account.account.description == entity.description
    assert sub_account.account.dept == entity.dept
    assert sub_account.account.bs_pl == entity.bs_pl
    assert sub_account.account.credit_debit == entity.credit_debit
