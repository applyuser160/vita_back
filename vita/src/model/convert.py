from vita.src.model.model import (
    Account,
    JournalEntry,
    SubAccount,
    Tunion as TunionModel,
)
from vita.src.util.sql_model import T as Tmodel
from vita.src.model.graphql_input import (
    T as Tinput,
    AccountGraphqlInput,
    InnerJournalEntryGraphqlInput,
    JournalEntryGraphqlInput,
    SubAccountGraphqlInput,
    Tunion as TunionInput,
)
from vita.src.model.graphql_type import (
    T as Ttype,
    AccountGraphqlType,
    InnerJournalEntryGraphqlType,
    JournalEntryGraphqlType,
    SubAccountGraphqlType,
    Tunion as TunionType,
)


class GraphqlConvert:

    @classmethod
    def get_input(cls, model: Tmodel) -> type[TunionInput]:
        if isinstance(model, Account):
            return AccountGraphqlInput
        elif isinstance(model, SubAccount):
            return SubAccountGraphqlInput
        elif isinstance(model, JournalEntry):
            return JournalEntryGraphqlInput
        else:
            return InnerJournalEntryGraphqlInput

    @classmethod
    def get_type(cls, model: Tmodel) -> type[TunionType]:
        if isinstance(model, Account):
            return AccountGraphqlType
        elif isinstance(model, SubAccount):
            return SubAccountGraphqlType
        elif isinstance(model, JournalEntry):
            return JournalEntryGraphqlType
        else:
            return InnerJournalEntryGraphqlType

    @classmethod
    def input_to_model(cls, model: Tmodel, input: Tinput) -> Tmodel:
        keys = [
            key
            for key in vars(model).keys()
            if not key.startswith("_") and key not in ["model_config"]
        ]
        result: Tmodel = model()
        for key in keys:
            try:
                value = input.__getattribute__(key)
            except AttributeError:
                continue
            if isinstance(value, list):
                value = [inner.to_pydantic() for inner in value]
            elif isinstance(value, TunionInput):
                value = value.to_pydantic()  # type: ignore
            result.__setattr__(key, value)
        return result

    @classmethod
    def type_to_model(cls, model: Tmodel, type: Ttype) -> Tmodel:
        keys = [
            key
            for key in vars(model).keys()
            if not key.startswith("_") and key not in ["model_config"]
        ]
        result: Tmodel = model()
        for key in keys:
            try:
                value = type.__getattribute__(key)
            except AttributeError:
                continue
            if isinstance(value, list):
                value = [inner.to_pydantic() for inner in value]
            elif isinstance(value, TunionType):
                value = value.to_pydantic()  # type: ignore
            result.__setattr__(key, value)
        return result

    @classmethod
    def model_to_input(cls, input: Tinput, model: Tmodel) -> Tinput:
        keys = [
            key
            for key in vars(model).keys()
            if not key.startswith("_") and key not in ["model_config"]
        ]
        result: Tinput = input.from_pydantic(model)  # type: ignore
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
            elif isinstance(value, TunionModel):
                _type = cls.get_input(value)
                value = _type.from_pydantic(value)  # type: ignore
            result.__setattr__(key, value)
        return result

    @classmethod
    def model_to_type(cls, type: Ttype, model: Tmodel) -> Ttype:
        keys = [
            key
            for key in vars(model).keys()
            if not key.startswith("_") and key not in ["model_config"]
        ]
        result: Ttype = type.from_pydantic(model)  # type: ignore
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
            elif isinstance(value, TunionModel):
                _type = cls.get_type(value)
                value = _type.from_pydantic(value)  # type: ignore
            result.__setattr__(key, value)
        return result
