import strawberry
from model.model import Account


@strawberry.type
class Query:

    @strawberry.field
    def hello(self) -> str:
        return "world"

    @strawberry.field
    def account(self) -> str:
        account = Account()
        return account.id
