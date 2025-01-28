from vita.src.model.model import (
    Account,
    BsPlEnum,
    CreditDebitEnum,
    DeptEnum,
    SubAccount,
)
from vita.src.model.graphql_input import AccountGraphqlInput, SubAccountGraphqlInput
from vita.src.model.graphql_type import AccountGraphqlType, SubAccountGraphqlType
from vita.src.model.convert import GraphqlConvert
from vita.src.util.constant import SYSTEM_USER
from vita.src.util.dt import VitaDatetime
from vita.src.util.sql_model import SQLSession


def test_input_to_model_case01():
    """
    テスト観点:
    一対多の接続があるモデル
    """

    input = AccountGraphqlInput(
        id="id",
        create_date=VitaDatetime(2025, 1, 1),
        create_object_id="create",
        update_date=VitaDatetime(2025, 1, 1),
        update_object_id="update",
        name="account name",
        description="description",
        dept=DeptEnum.CURRENT_ASSETS,
        bs_pl=BsPlEnum.BS,
        credit_debit=CreditDebitEnum.CREDIT,
        sub_accounts=[
            SubAccountGraphqlInput(
                name="sub account",
                account_id="id",
                description="desc",
            )
        ],
    )

    assert input.sub_accounts

    result = GraphqlConvert.input_to_model(Account, input)

    assert isinstance(result, Account)
    assert result.id
    assert result.id == "id"
    assert result.create_date
    assert result.create_date == VitaDatetime(2025, 1, 1)
    assert result.create_object_id
    assert result.create_object_id == "create"
    assert result.update_date
    assert result.update_date == VitaDatetime(2025, 1, 1)
    assert result.update_object_id
    assert result.update_object_id == "update"
    assert result.name == "account name"
    assert result.description
    assert result.description == "description"
    assert result.dept == DeptEnum.CURRENT_ASSETS
    assert result.bs_pl == BsPlEnum.BS
    assert result.credit_debit == CreditDebitEnum.CREDIT
    assert result.sub_accounts
    assert len(result.sub_accounts) == 1
    assert result.sub_accounts[0].name == "sub account"
    assert result.sub_accounts[0].account_id == "id"
    assert result.sub_accounts[0].description == "desc"
    assert not result.inner_journal_entries_account


def test_input_to_model_case02():
    """
    テスト観点:
    多対一の接続があるモデル
    """
    input = SubAccountGraphqlInput(
        name="sub account",
        account_id="id",
        description="desc",
        account=AccountGraphqlInput(
            id="id",
            create_date=VitaDatetime.now(),
            create_object_id="create",
            update_date=VitaDatetime.now(),
            update_object_id="update",
            name="account name",
            description="description",
            dept=DeptEnum.CURRENT_ASSETS,
            bs_pl=BsPlEnum.BS,
            credit_debit=CreditDebitEnum.CREDIT,
        ),
    )

    assert input.account

    result = GraphqlConvert.input_to_model(SubAccount, input)

    assert isinstance(result, SubAccount)
    assert result.name == "sub account"
    assert result.account.id == "id"


def test_input_to_model_case03(session: SQLSession):
    """
    テスト観点:
    DBへレコードを挿入
    """
    input = AccountGraphqlInput(
        id="id",
        create_date=VitaDatetime(2025, 1, 1),
        create_object_id="create",
        update_date=VitaDatetime(2025, 1, 1),
        update_object_id="update",
        name="account name",
        description="description",
        dept=DeptEnum.CURRENT_ASSETS,
        bs_pl=BsPlEnum.BS,
        credit_debit=CreditDebitEnum.CREDIT,
        sub_accounts=[
            SubAccountGraphqlInput(
                name="sub account",
                account_id="id",
                description="desc",
            )
        ],
    )

    assert input.sub_accounts

    model = GraphqlConvert.input_to_model(Account, input)
    inner_models = GraphqlConvert.copy_models(model.sub_accounts)

    model = session.save(Account, model, SYSTEM_USER)
    # session.session.refresh(model)
    inner_model = session.save(SubAccount, inner_models[0], SYSTEM_USER)
    # session.session.refresh(inner_model)

    assert model
    assert inner_model

    records = session.find(Account, isOne=False)
    inner_records = session.find(SubAccount, isOne=False)

    assert len(records) == 1
    assert len(inner_records) == 1


def test_type_to_model_case01():
    """
    テスト観点:
    一対多の接続があるモデル
    """
    type = AccountGraphqlType(
        id="id",
        create_date=VitaDatetime(2025, 1, 1),
        create_object_id="create",
        update_date=VitaDatetime(2025, 1, 1),
        update_object_id="update",
        name="account name",
        description="description",
        dept=DeptEnum.CURRENT_ASSETS,
        bs_pl=BsPlEnum.BS,
        credit_debit=CreditDebitEnum.CREDIT,
        sub_accounts=[
            SubAccountGraphqlType(
                name="sub account",
                account_id="id",
                description="desc",
            )
        ],
    )

    assert type.sub_accounts

    result = GraphqlConvert.type_to_model(Account, type)

    assert isinstance(result, Account)
    assert result.id
    assert result.id == "id"
    assert result.create_date
    assert result.create_date == VitaDatetime(2025, 1, 1)
    assert result.create_object_id
    assert result.create_object_id == "create"
    assert result.update_date
    assert result.update_date == VitaDatetime(2025, 1, 1)
    assert result.update_object_id
    assert result.update_object_id == "update"
    assert result.name == "account name"
    assert result.description
    assert result.description == "description"
    assert result.dept == DeptEnum.CURRENT_ASSETS
    assert result.bs_pl == BsPlEnum.BS
    assert result.credit_debit == CreditDebitEnum.CREDIT
    assert result.sub_accounts
    assert len(result.sub_accounts) == 1
    assert result.sub_accounts[0].name == "sub account"
    assert result.sub_accounts[0].account_id == "id"
    assert result.sub_accounts[0].description == "desc"
    assert not result.inner_journal_entries_account


def test_type_to_model_case02():
    """
    テスト観点:
    多対一の接続があるモデル
    """
    type = SubAccountGraphqlType(
        name="sub account",
        account_id="id",
        description="desc",
        account=AccountGraphqlType(
            id="id",
            create_date=VitaDatetime.now(),
            create_object_id="create",
            update_date=VitaDatetime.now(),
            update_object_id="update",
            name="account name",
            description="description",
            dept=DeptEnum.CURRENT_ASSETS,
            bs_pl=BsPlEnum.BS,
            credit_debit=CreditDebitEnum.CREDIT,
        ),
    )

    assert type.account

    result = GraphqlConvert.type_to_model(SubAccount, type)

    assert isinstance(result, SubAccount)
    assert result.name == "sub account"
    assert result.account
    assert result.account.id == "id"


def test_model_to_input_case01():
    """
    テスト観点:
    一対多の接続があるモデル
    """
    sub_account = SubAccount(
        name="sub account",
        account_id="id",
        description="desc",
    )

    account = Account(
        id="id",
        create_date=VitaDatetime.now(),
        create_object_id="create",
        update_date=VitaDatetime.now(),
        update_object_id="update",
        name="account name",
        description="description",
        dept=DeptEnum.CURRENT_ASSETS,
        bs_pl=BsPlEnum.BS,
        credit_debit=CreditDebitEnum.CREDIT,
        sub_accounts=[sub_account],
    )

    result: AccountGraphqlInput = GraphqlConvert.model_to_input(
        AccountGraphqlInput, account
    )

    assert isinstance(result, AccountGraphqlInput)
    assert result.id
    assert result.id == account.id
    assert result.create_date
    assert result.create_date == account.create_date
    assert result.create_object_id
    assert result.create_object_id == account.create_object_id
    assert result.update_date
    assert result.update_date == account.update_date
    assert result.update_object_id
    assert result.update_object_id == account.update_object_id
    assert result.name == account.name
    assert result.description
    assert result.description == account.description
    assert result.dept == account.dept
    assert result.bs_pl == account.bs_pl
    assert result.credit_debit == account.credit_debit
    assert result.sub_accounts
    assert len(result.sub_accounts) == 1
    assert result.sub_accounts[0].name == sub_account.name
    assert result.sub_accounts[0].account_id == sub_account.account_id
    assert result.sub_accounts[0].description == sub_account.description


def test_model_to_type_case01():
    """
    テスト観点:
    一対多の接続があるモデル
    """
    account = Account(
        id="id",
        create_date=VitaDatetime.now(),
        create_object_id="create",
        update_date=VitaDatetime.now(),
        update_object_id="update",
        name="account name",
        description="description",
        dept=DeptEnum.CURRENT_ASSETS,
        bs_pl=BsPlEnum.BS,
        credit_debit=CreditDebitEnum.CREDIT,
    )
    sub_account = SubAccount(
        name="sub account",
        account_id="id",
        description="desc",
        account=account,
    )

    result = GraphqlConvert.model_to_type(SubAccountGraphqlType, sub_account)

    assert isinstance(result, SubAccountGraphqlType)
