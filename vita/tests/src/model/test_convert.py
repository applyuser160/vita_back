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
from vita.src.util.dt import VitaDatetime


def test_input_to_model_case01():
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
    )

    input = AccountGraphqlInput.from_pydantic(account)
    input.__setattr__(
        "sub_accounts", [SubAccountGraphqlInput.from_pydantic(sub_account)]
    )

    assert input.sub_accounts

    result = GraphqlConvert.input_to_model(Account, input)

    assert isinstance(result, Account)
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
    assert not result.inner_journal_entries_account


def test_input_to_model_case02():
    """
    テスト観点:
    多対一の接続があるモデル
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
    )

    input = SubAccountGraphqlInput.from_pydantic(sub_account)
    input.__setattr__("account", AccountGraphqlInput.from_pydantic(account))

    assert input.account

    result = GraphqlConvert.input_to_model(SubAccount, input)

    assert isinstance(result, SubAccount)
    assert result.name == sub_account.name
    assert result.account.id == account.id


def test_type_to_model_case01():
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
    )

    type = AccountGraphqlType.from_pydantic(account)
    type.__setattr__("sub_accounts", [SubAccountGraphqlType.from_pydantic(sub_account)])

    assert type.sub_accounts

    result = GraphqlConvert.type_to_model(Account, type)

    assert isinstance(result, Account)
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
    assert not result.inner_journal_entries_account


def test_type_to_model_case02():
    """
    テスト観点:
    多対一の接続があるモデル
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
    )

    type = SubAccountGraphqlType.from_pydantic(sub_account)
    type.__setattr__("account", AccountGraphqlType.from_pydantic(account))

    assert type.account

    result = GraphqlConvert.type_to_model(SubAccount, type)

    assert isinstance(result, SubAccount)
    assert result.name == sub_account.name
    assert result.account.id == account.id


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

    result = GraphqlConvert.model_to_type(AccountGraphqlType, account)
    assert isinstance(result, AccountGraphqlType)
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
