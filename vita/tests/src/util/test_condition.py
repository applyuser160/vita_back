from vita.src.model.model import Account
from vita.src.util.condition import Condition, ConditionType


def test_condition():
    condition = Condition(Account.id, ConditionType.EQUAL, 1, False)
    assert condition

    account = Account()
    assert not account.id
