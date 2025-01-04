from vita.src.model.graphql_input import AccountsGraphqlInput
from vita.src.model.model import (
    Account,
    BsPlEnum,
    CreditDebitEnum,
    DeptEnum,
    SubAccount,
)
from vita.src.service.get_accounts_service import GetAccountsService
from vita.src.util.constant import SYSTEM_USER
from vita.src.util.sql_model import SQLSession
from vita.src.model.convert import GraphqlConvert


def test_get_account_service_case01(session: SQLSession):
    entities = [
        Account(
            name="name1",
            description="des1",
            dept=DeptEnum.CURRENT_ASSETS,
            bs_pl=BsPlEnum.BS,
            credit_debit=CreditDebitEnum.DEBIT,
        ),
        Account(
            name="name2",
            description="des2",
            dept=DeptEnum.DEFERRED_ASSETS,
            bs_pl=BsPlEnum.PL,
            credit_debit=CreditDebitEnum.CREDIT,
        ),
    ]
    entities = session.bulk_save(entities, SYSTEM_USER)

    sub_entity = SubAccount(
        name="name",
        account_id=entities[0].id,
        description="desc",
    )
    sub_entity = session.save(SubAccount, sub_entity, SYSTEM_USER)

    input = AccountsGraphqlInput(
        name=None,
        description=None,
        dept=None,
        bs_pl=None,
        credit_debit=None,
    )
    results = GetAccountsService(session).execute(input)

    accounts = [GraphqlConvert.type_to_model(Account, result) for result in results]

    assert len(accounts) == 2

    assert accounts[0].name == entities[0].name
    assert accounts[0].description == entities[0].description
    assert accounts[0].dept == entities[0].dept
    assert accounts[0].bs_pl == entities[0].bs_pl
    assert accounts[0].credit_debit == entities[0].credit_debit
    assert len(accounts[0].sub_accounts) == 1
    assert accounts[0].sub_accounts[0].name == sub_entity.name
    assert accounts[0].sub_accounts[0].description == sub_entity.description

    assert accounts[1].name == entities[1].name
    assert accounts[1].description == entities[1].description
    assert accounts[1].dept == entities[1].dept
    assert accounts[1].bs_pl == entities[1].bs_pl
    assert accounts[1].credit_debit == entities[1].credit_debit
    assert len(accounts[1].sub_accounts) == 0
