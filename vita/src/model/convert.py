from vita.src.util.sql_model import T as Tmodel
from vita.src.model.graphql_input import T as Tinput, Tunion as TunionInput
from vita.src.model.graphql_type import T as Ttype, Tunion as TunionType


class GraphqlConvert:

    @staticmethod
    def input_to_model(model: Tmodel, input: Tinput) -> Tmodel:
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

    @staticmethod
    def type_to_model(model: Tmodel, type: Ttype) -> Tmodel:
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
