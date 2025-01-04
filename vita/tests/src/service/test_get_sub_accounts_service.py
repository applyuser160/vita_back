from vita.src.model.graphql_input import SubAccountsGraphqlInput
from vita.src.model.model import (
    Account,
    BsPlEnum,
    CreditDebitEnum,
    DeptEnum,
    SubAccount,
)
from vita.src.service.get_sub_accounts_service import GetSubAccountsService
from vita.src.util.constant import SYSTEM_USER
from vita.src.util.sql_model import SQLSession
from vita.src.model.convert import GraphqlConvert


def test_get_sub_accounts_service_case01(session: SQLSession):
    entity = Account(
        name="name",
        description="des",
        dept=DeptEnum.CURRENT_ASSETS,
        bs_pl=BsPlEnum.BS,
        credit_debit=CreditDebitEnum.DEBIT,
    )
    entity = session.save(Account, entity, SYSTEM_USER)

    sub_entities = [
        SubAccount(
            name="name1",
            account_id=entity.id,
            description="desc1",
        ),
        SubAccount(
            name="name2",
            account_id=entity.id,
            description="desc2",
        ),
    ]
    sub_entities = session.bulk_save(sub_entities, SYSTEM_USER)

    input = SubAccountsGraphqlInput(
        name=None,
        description=None,
        account_id=None,
    )
    results = GetSubAccountsService(session).execute(input)

    sub_accounts = [
        GraphqlConvert.type_to_model(SubAccount, result) for result in results
    ]

    assert len(sub_entities) == 2

    assert sub_accounts[0].name == sub_entities[0].name
    assert sub_accounts[0].description == sub_entities[0].description
    assert sub_accounts[0].account
    assert sub_accounts[0].account.name == entity.name
    assert sub_accounts[0].account.description == entity.description
    assert sub_accounts[0].account.dept == entity.dept
    assert sub_accounts[0].account.bs_pl == entity.bs_pl
    assert sub_accounts[0].account.credit_debit == entity.credit_debit

    assert sub_accounts[1].name == sub_entities[1].name
    assert sub_accounts[1].description == sub_entities[1].description
