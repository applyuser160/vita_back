from __future__ import annotations

from enum import Enum
from typing import Any
from sqlmodel import col
from sqlalchemy import BinaryExpression, Column


class ConditionType(Enum):
    EQUAL = 0
    NOT_EQUAL = 1
    GREATER_THAN = 2
    GREATER = 3
    LESS_THAN = 4
    LESS = 5
    CONTAINS = 6
    LIKE = 7


class Condition:
    target: Column  # type: ignore
    type: ConditionType
    value: Any  # type: ignore
    isnot: bool

    def __init__(self, target: Column, type: ConditionType, value: Any, isnot: bool):
        self.target = col(target)
        self.type = type
        self.value = value
        self.isnot = isnot

    def to_sqlachemy(self) -> BinaryExpression:
        if type == ConditionType.EQUAL:
            result = self.target == self.value  # type: ignore
        elif type == ConditionType.NOT_EQUAL:
            result = self.target != self.value
        elif type == ConditionType.GREATER_THAN:
            result = self.target >= self.value
        elif type == ConditionType.GREATER:
            result = self.target > self.value
        elif type == ConditionType.LESS_THAN:
            result = self.target <= self.value
        elif type == ConditionType.LESS:
            result = self.target < self.value
        elif type == ConditionType.CONTAINS:
            result = self.target.contains(self.value)
        else:
            result = self.target.like(f"%{self.value}%")

        return not result if self.isnot else result
