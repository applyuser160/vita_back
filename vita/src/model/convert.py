from vita.src.model.model import (
    Account,
    JournalEntry,
    SubAccount,
    ModelUnion,
)
from vita.src.util.sql_model import T
from vita.src.model.graphql_input import (
    I,
    AccountGraphqlInput,
    InnerJournalEntryGraphqlInput,
    JournalEntryGraphqlInput,
    SubAccountGraphqlInput,
    InputUnion,
)
from vita.src.model.graphql_type import (
    Y,
    AccountGraphqlType,
    InnerJournalEntryGraphqlType,
    JournalEntryGraphqlType,
    SubAccountGraphqlType,
    TypeUnion,
)


class GraphqlConvert:

    @classmethod
    def get_input(cls, model: T) -> type[InputUnion]:
        if isinstance(model, Account):
            return AccountGraphqlInput
        elif isinstance(model, SubAccount):
            return SubAccountGraphqlInput
        elif isinstance(model, JournalEntry):
            return JournalEntryGraphqlInput
        else:
            return InnerJournalEntryGraphqlInput

    @classmethod
    def get_type(cls, model: T) -> type[TypeUnion]:
        if isinstance(model, Account):
            return AccountGraphqlType
        elif isinstance(model, SubAccount):
            return SubAccountGraphqlType
        elif isinstance(model, JournalEntry):
            return JournalEntryGraphqlType
        else:
            return InnerJournalEntryGraphqlType

    @classmethod
    def input_to_model(cls, model: type[T], input: I) -> T:
        keys = [
            key
            for key in vars(input).keys()
            if not key.startswith("_") and key not in ["model_config"]
        ]
        result = model()
        for key in keys:
            try:
                value = input.__getattribute__(key)
            except AttributeError:
                continue
            if isinstance(value, list):
                value = [inner.to_pydantic() for inner in value]
            elif isinstance(value, InputUnion):
                value = value.to_pydantic()  # type: ignore
            result.__setattr__(key, value)
        return result

    @classmethod
    def type_to_model(cls, model: type[T], type: Y) -> T:
        keys = [
            key
            for key in vars(model).keys()
            if not key.startswith("_") and key not in ["model_config"]
        ]
        result = model()
        for key in keys:
            try:
                value = type.__getattribute__(key)
            except AttributeError:
                continue
            if isinstance(value, list):
                value = [inner.to_pydantic() for inner in value]
            elif isinstance(value, TypeUnion):
                value = value.to_pydantic()  # type: ignore
            result.__setattr__(key, value)
        return result

    @classmethod
    def model_to_input(cls, input: type[I], model: T) -> I:
        keys = [
            key
            for key in vars(model).keys()
            if not key.startswith("_") and key not in ["model_config"]
        ]
        result = input.from_pydantic(model)  # type: ignore
        for key in keys:
            try:
                value = model.__getattribute__(key)
            except AttributeError:
                continue
            if isinstance(value, list):
                if not value:
                    continue
                _type = cls.get_input(value[0])
                value = [_type.from_pydantic(inner) for inner in value]  # type: ignore
            elif isinstance(value, ModelUnion):
                _type = cls.get_input(value)
                value = _type.from_pydantic(value)  # type: ignore
            result.__setattr__(key, value)
        return result

    @classmethod
    def model_to_type(cls, type: type[Y], model: T) -> Y:
        keys = [
            key
            for key in vars(model).keys()
            if not key.startswith("_") and key not in ["model_config"]
        ]
        result = type.from_pydantic(model)  # type: ignore
        for key in keys:
            try:
                value = model.__getattribute__(key)
            except AttributeError:
                continue
            if isinstance(value, list):
                if not value:
                    continue
                _type = cls.get_type(value[0])
                value = [_type.from_pydantic(inner) for inner in value]  # type: ignore
            elif isinstance(value, ModelUnion):
                _type = cls.get_type(value)
                value = _type.from_pydantic(value)  # type: ignore
            result.__setattr__(key, value)
        return result
