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
from vita.src.service.get_account_service import GetAccountService
from vita.src.service.get_accounts_service import GetAccountsService
from vita.src.service.get_journal_entries_service import GetJournalEntriesService
from vita.src.service.get_journal_entry_service import GetJournalEntryService
from vita.src.service.get_sub_account_service import GetSubAccountService
from vita.src.service.get_sub_accounts_service import GetSubAccountsService
from vita.src.util.err import VitaError
from vita.src.util.logg import Logg
from vita.src.util.sql_model import SQLSession


@strawberry.type
class Query:

    def get_session(self):
        return SQLSession(Logg())

    @strawberry.field
    def account(self, input: SingleGraphqlInput) -> AccountGraphqlType | VitaError:
        return GetAccountService(self.get_session()).execute(input)

    @strawberry.field
    def accounts(
        self, input: AccountsGraphqlInput
    ) -> list[AccountGraphqlType] | VitaError:
        return GetAccountsService(self.get_session()).execute(input)

    @strawberry.field
    def sub_account(
        self, input: SingleGraphqlInput
    ) -> SubAccountGraphqlType | VitaError:
        return GetSubAccountService(self.get_session()).execute(input)

    @strawberry.field
    def sub_accounts(
        self, input: SubAccountsGraphqlInput
    ) -> list[SubAccountGraphqlType] | VitaError:
        return GetSubAccountsService(self.get_session()).execute(input)

    @strawberry.field
    def journal_entry(
        self, input: SingleGraphqlInput
    ) -> JournalEntryGraphqlType | VitaError:
        return GetJournalEntryService(self.get_session()).execute(input)

    @strawberry.field
    def journal_entries(
        self, input: JournalEntriesGraphqlInput
    ) -> list[JournalEntryGraphqlType] | VitaError:
        return GetJournalEntriesService(self.get_session()).execute(input)
