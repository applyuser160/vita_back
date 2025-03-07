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
    IN = 8


class Condition:
    target: Column
    type: ConditionType
    value: Any  # type: ignore
    isnot: bool

    def __init__(
        self, target: Column, type: ConditionType, value: Any, isnot: bool = False
    ):
        self.target = col(target)
        self.type = type
        self.value = value
        self.isnot = isnot

    def to_sqlachemy(self) -> BinaryExpression:
        match self.type:
            case ConditionType.EQUAL:
                result = (
                    col(self.target).is_(self.value)
                    if self.value is None
                    else self.target == self.value
                )
            case ConditionType.NOT_EQUAL:
                result = (
                    col(self.target).is_not(self.value)
                    if self.value is None
                    else self.target != self.value
                )
            case ConditionType.GREATER_THAN:
                result = self.target >= self.value
            case ConditionType.GREATER:
                result = self.target > self.value
            case ConditionType.LESS_THAN:
                result = self.target <= self.value
            case ConditionType.LESS:
                result = self.target < self.value
            case ConditionType.CONTAINS:
                result = self.target.contains(self.value)
            case ConditionType.IN:
                result = self.target.in_(self.value)
            case _:
                result = self.target.like(f"%{self.value}%")

        return not result if self.isnot else result
