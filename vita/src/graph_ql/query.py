import strawberry
from model.graphql_type import AccountGraphqlType
from model.model import Account
from util.err import VitaError


@strawberry.type
class Query:

    @strawberry.field
    def account(self) -> AccountGraphqlType | VitaError:
        account = Account()
        if account:
            return AccountGraphqlType.from_pydantic(account)
        return VitaError(1, "error")
