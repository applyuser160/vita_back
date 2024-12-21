import strawberry
from model.graphql_input import (
    AccountGraphqlInput,
    InnerJournalEntryGraphqlInput,
    JournalEntryGraphqlInput,
    SubAccountGraphqlInput,
)
from model.graphql_type import (
    AccountGraphqlType,
    InnerJournalEntryGraphqlType,
    JournalEntryGraphqlType,
    SubAccountGraphqlType,
)
from service.create_account_service import CreateAccountService
from util.err import VitaError


@strawberry.type
class Mutation:

    @strawberry.mutation
    def create_account(
        self, input: AccountGraphqlInput
    ) -> AccountGraphqlType | VitaError:
        return CreateAccountService().execute(input)

    @strawberry.mutation
    def update_account(
        self, input: AccountGraphqlInput
    ) -> AccountGraphqlType | VitaError:
        pass

    @strawberry.mutation
    def delete_account(
        self, input: AccountGraphqlInput
    ) -> AccountGraphqlType | VitaError:
        pass

    @strawberry.mutation
    def create_sub_account(
        self, input: SubAccountGraphqlInput
    ) -> SubAccountGraphqlType | VitaError:
        pass

    @strawberry.mutation
    def update_sub_account(
        self, input: SubAccountGraphqlInput
    ) -> SubAccountGraphqlType | VitaError:
        pass

    @strawberry.mutation
    def delete_sub_account(
        self, input: SubAccountGraphqlInput
    ) -> SubAccountGraphqlType | VitaError:
        pass

    @strawberry.mutation
    def create_journal_entry(
        self, input: JournalEntryGraphqlInput
    ) -> JournalEntryGraphqlType | VitaError:
        pass

    @strawberry.mutation
    def update_journal_entry(
        self, input: JournalEntryGraphqlInput
    ) -> JournalEntryGraphqlType | VitaError:
        pass

    @strawberry.mutation
    def delete_journal_entry(
        self, input: JournalEntryGraphqlInput
    ) -> JournalEntryGraphqlType | VitaError:
        pass
