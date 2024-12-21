import strawberry
from model.graphql_input import (
    AccountsGraphqlInput,
    JournalEntriesGraphqlInput,
    SingleGraphqlInput,
    SubAccountsGraphqlInput,
)
from model.graphql_type import (
    AccountGraphqlType,
    JournalEntryGraphqlType,
    SubAccountGraphqlType,
)
from model.model import Account
from util.err import VitaError


@strawberry.type
class Query:

    @strawberry.field
    def account(self, input: SingleGraphqlInput) -> AccountGraphqlType | VitaError:
        pass

    @strawberry.field
    def accounts(
        self, input: AccountsGraphqlInput
    ) -> list[AccountGraphqlType] | VitaError:
        pass

    @strawberry.field
    def sub_account(
        self, input: SingleGraphqlInput
    ) -> SubAccountGraphqlType | VitaError:
        pass

    @strawberry.field
    def sub_accounts(
        self, input: SubAccountsGraphqlInput
    ) -> list[SubAccountGraphqlType] | VitaError:
        pass

    @strawberry.field
    def journal_entry(
        self, input: SingleGraphqlInput
    ) -> JournalEntryGraphqlType | VitaError:
        pass

    @strawberry.field
    def journal_entries(
        self, input: JournalEntriesGraphqlInput
    ) -> list[JournalEntryGraphqlType] | VitaError:
        pass
