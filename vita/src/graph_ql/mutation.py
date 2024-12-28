import strawberry
from model.graphql_input import (
    AccountGraphqlInput,
    JournalEntryGraphqlInput,
    SubAccountGraphqlInput,
)
from model.graphql_type import (
    AccountGraphqlType,
    JournalEntryGraphqlType,
    SubAccountGraphqlType,
)
from vita.src.service.create_account_service import CreateAccountService
from vita.src.service.update_account_service import UpdateAccountService
from vita.src.service.delete_account_service import DeleteAccountService
from vita.src.util.err import VitaError
from vita.src.util.sql_model import SQLSession
from vita.src.util.logg import Logg


@strawberry.type
class Mutation:

    def get_session(self):
        return SQLSession(Logg())

    @strawberry.mutation
    def create_account(
        self, input: AccountGraphqlInput
    ) -> AccountGraphqlType | VitaError:
        return CreateAccountService(self.get_session()).execute(input)

    @strawberry.mutation
    def update_account(
        self, input: AccountGraphqlInput
    ) -> AccountGraphqlType | VitaError:
        return UpdateAccountService(self.get_session()).execute(input)

    @strawberry.mutation
    def delete_account(
        self, input: AccountGraphqlInput
    ) -> AccountGraphqlType | VitaError:
        return DeleteAccountService(self.get_session()).execute(input)

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
