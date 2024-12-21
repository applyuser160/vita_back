from vita.src.util.condition import Condition, ConditionType


def test_condition():
    condition = Condition(1, ConditionType.EQUAL, 1, False)
    assert condition
