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
from vita.src.util.err import VitaError
from vita.src.util.logg import Logg
from vita.src.util.sql_model import SQLSession


@strawberry.type
class Query:

    def get_session(self):
        return SQLSession(Logg())

    @strawberry.field
    def account(self, input: SingleGraphqlInput) -> AccountGraphqlType | VitaError:
        pass

    @strawberry.field
    def accounts(
        self, input: AccountsGraphqlInput
    ) -> list[AccountGraphqlType] | VitaError:
        return []

    @strawberry.field
    def sub_account(
        self, input: SingleGraphqlInput
    ) -> SubAccountGraphqlType | VitaError:
        pass

    @strawberry.field
    def sub_accounts(
        self, input: SubAccountsGraphqlInput
    ) -> list[SubAccountGraphqlType] | VitaError:
        return []

    @strawberry.field
    def journal_entry(
        self, input: SingleGraphqlInput
    ) -> JournalEntryGraphqlType | VitaError:
        pass

    @strawberry.field
    def journal_entries(
        self, input: JournalEntriesGraphqlInput
    ) -> list[JournalEntryGraphqlType] | VitaError:
        return []
