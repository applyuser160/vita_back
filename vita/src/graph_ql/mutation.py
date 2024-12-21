import strawberry


@strawberry.type
class Mutation:

    @strawberry.mutation
    def hello(self) -> str:
        return "world"
