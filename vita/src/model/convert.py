from vita.src.model.model import (
    Account,
    Balance,
    DailyBalance,
    InnerJournalEntry,
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
    BalanceGraphqlType,
    DailyBalanceGraphqlType,
    InnerJournalEntryGraphqlType,
    JournalEntryGraphqlType,
    SubAccountGraphqlType,
    TypeUnion,
)


class AttributeInfo:
    name: str
    is_relatinship: bool
    use_list: bool

    def __init__(self, name: str, is_relatinship: bool, use_list: bool):
        self.name = name
        self.is_relatinship = is_relatinship
        self.use_list = use_list


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
        elif isinstance(model, InnerJournalEntry):
            return InnerJournalEntryGraphqlType
        elif isinstance(model, Balance):
            return BalanceGraphqlType
        else:
            return DailyBalanceGraphqlType

    @classmethod
    def get_model(
        cls,
        input: InputUnion | None = None,
        type: TypeUnion | None = None,
    ) -> type[T]:
        if input:
            if isinstance(input, AccountGraphqlInput):
                return Account
            elif isinstance(input, SubAccountGraphqlInput):
                return SubAccount
            elif isinstance(input, JournalEntryGraphqlInput):
                return JournalEntry
            else:
                return InnerJournalEntry
        elif type:
            if isinstance(type, AccountGraphqlType):
                return Account
            elif isinstance(type, SubAccountGraphqlType):
                return SubAccount
            elif isinstance(type, JournalEntryGraphqlType):
                return JournalEntry
            elif isinstance(type, InnerJournalEntryGraphqlType):
                return InnerJournalEntry
            elif isinstance(type, BalanceGraphqlType):
                return Balance
            else:
                return DailyBalance
        else:
            raise ValueError("input and type are none.")

    @classmethod
    def copy_models(cls, models: list[T]) -> list[T]:
        return [
            type(model)(
                **{
                    k: v
                    for k, v in model.model_dump().items()
                    if k in type(model).model_fields.keys() and v
                }
            )
            for model in models
        ]

    @classmethod
    def copy_model(cls, model: T) -> T:
        return type(model)(
            **{
                k: v
                for k, v in model.model_dump().items()
                if k in type(model).model_fields.keys() and v
            }
        )

    @classmethod
    def get_graphql_to_dict(cls, graphql_obj: InputUnion | TypeUnion) -> dict:
        return {
            k: v
            for k, v in vars(graphql_obj).items()
            if not k.startswith("_") and k not in ["model_config"]
        }

    @classmethod
    def get_relationship_type(cls, model: type[T], field_name: str) -> type[T]:
        field = model.model_fields[field_name]
        if field.annotation.__origin__ == list:
            return field.annotation.__args__[0]
        return field.annotation

    @classmethod
    def input_to_model(cls, model: type[T], input: I) -> T:
        columns, relatinships, uselists = model().get_columns_and_relationships()
        attributes: list[AttributeInfo] = [
            *[
                AttributeInfo(name=i, is_relatinship=False, use_list=False)
                for i in columns  # type: ignore
            ],
            *[
                AttributeInfo(name=relationship, is_relatinship=True, use_list=uselist)
                for relationship, uselist in zip(relatinships, uselists)  # type: ignore
            ],
        ]

        attrs: dict = {}
        for attribute in attributes:
            try:
                value = input.__getattribute__(attribute.name)
            except AttributeError:
                value = None

            if attribute.use_list:
                if isinstance(value, list):
                    value = [
                        cls.get_model(input=inner)(  # type: ignore
                            **{
                                k: v
                                for k, v in cls.get_graphql_to_dict(inner).items()
                                if v
                            }
                        )
                        for inner in value
                    ]
                else:
                    value = []
            elif attribute.is_relatinship:
                if isinstance(value, InputUnion):
                    value = cls.get_model(input=value)(  # type: ignore
                        **{k: v for k, v in cls.get_graphql_to_dict(value).items() if v}
                    )
                else:
                    value = None

            attrs[attribute.name] = value

        return model(**attrs)

    @classmethod
    def type_to_model(cls, model: type[T], type: Y) -> T:
        columns, relatinships, uselists = model().get_columns_and_relationships()
        attributes: list[AttributeInfo] = [
            *[
                AttributeInfo(name=i, is_relatinship=False, use_list=False)
                for i in columns  # type: ignore
            ],
            *[
                AttributeInfo(name=relationship, is_relatinship=True, use_list=uselist)
                for relationship, uselist in zip(relatinships, uselists)  # type: ignore
            ],
        ]

        attrs: dict = {}
        for attribute in attributes:
            try:
                value = type.__getattribute__(attribute.name)
            except AttributeError:
                value = None

            if attribute.use_list:
                if isinstance(value, list):
                    value = [
                        cls.get_model(type=inner)(  # type: ignore
                            **{
                                k: v
                                for k, v in cls.get_graphql_to_dict(inner).items()
                                if v
                            }
                        )
                        for inner in value
                    ]
                else:
                    value = []
            elif attribute.is_relatinship:
                if isinstance(value, TypeUnion):
                    value = cls.get_model(type=value)(  # type: ignore
                        **{k: v for k, v in cls.get_graphql_to_dict(value).items() if v}
                    )
                else:
                    value = None

            attrs[attribute.name] = value

        return model(**attrs)

    @classmethod
    def model_to_input(cls, input: type[I], model: T) -> I:
        keys = [
            key
            for key in vars(model).keys()
            if not key.startswith("_") and key not in ["model_config"]
        ]
        result = input(**model.extract_valid_value())
        for key in keys:
            try:
                value = model.__getattribute__(key)
            except AttributeError:
                continue
            if isinstance(value, list):
                if not value:
                    continue
                _type = cls.get_input(value[0])
                value = [_type(**inner.extract_valid_value()) for inner in value]
            elif isinstance(value, ModelUnion):
                _type = cls.get_input(value)
                value = _type(**value.extract_valid_value())
            result.__setattr__(key, value)
        return result

    @classmethod
    def model_to_type(cls, type: type[Y], model: T) -> Y:
        keys = [
            key
            for key in vars(model).keys()
            if not key.startswith("_") and key not in ["model_config"]
        ]
        result = type(**model.extract_valid_value())
        for key in keys:
            try:
                value = model.__getattribute__(key)
            except AttributeError:
                continue
            if isinstance(value, list):
                if not value:
                    continue
                _type = cls.get_type(value[0])
                value = [_type(**inner.extract_valid_value()) for inner in value]
            elif isinstance(value, ModelUnion):
                _type = cls.get_type(value)
                value = _type(**value.extract_valid_value())
            result.__setattr__(key, value)
        return result
