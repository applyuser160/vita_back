import strawberry
from vita.src.model.graphql_input import (
    AccountGraphqlInput,
    JournalEntryGraphqlInput,
    SubAccountGraphqlInput,
)
from vita.src.model.graphql_type import (
    AccountGraphqlType,
    JournalEntryGraphqlType,
    SubAccountGraphqlType,
    VitaErrorGraphqlType,
)
from vita.src.service.create_account_service import CreateAccountService
from vita.src.service.update_account_service import UpdateAccountService
from vita.src.service.delete_account_service import DeleteAccountService
from vita.src.service.create_sub_account_service import CreateSubAccountService
from vita.src.service.update_sub_account_service import UpdateSubAccountService
from vita.src.service.delete_sub_account_service import DeleteSubAccountService
from vita.src.service.create_journal_entry_serivce import CreateJournalEntryService
from vita.src.service.update_journal_entry_serivce import UpdateJournalEntryService
from vita.src.service.delete_journal_entry_serivce import DeleteJournalEntryService
from vita.src.util.sql_model import SQLSession
from vita.src.util.logg import Logg


@strawberry.type
class Mutation:

    @classmethod
    def get_session(self):
        return SQLSession(Logg())

    @strawberry.mutation
    def create_account(
        self, input: AccountGraphqlInput
    ) -> AccountGraphqlType | VitaErrorGraphqlType:
        return CreateAccountService(Mutation.get_session()).execute(input)

    @strawberry.mutation
    def update_account(
        self, input: AccountGraphqlInput
    ) -> AccountGraphqlType | VitaErrorGraphqlType:
        return UpdateAccountService(Mutation.get_session()).execute(input)

    @strawberry.mutation
    def delete_account(
        self, input: AccountGraphqlInput
    ) -> AccountGraphqlType | VitaErrorGraphqlType:
        return DeleteAccountService(Mutation.get_session()).execute(input)

    @strawberry.mutation
    def create_sub_account(
        self, input: SubAccountGraphqlInput
    ) -> SubAccountGraphqlType | VitaErrorGraphqlType:
        return CreateSubAccountService(Mutation.get_session()).execute(input)

    @strawberry.mutation
    def update_sub_account(
        self, input: SubAccountGraphqlInput
    ) -> SubAccountGraphqlType | VitaErrorGraphqlType:
        return UpdateSubAccountService(Mutation.get_session()).execute(input)

    @strawberry.mutation
    def delete_sub_account(
        self, input: SubAccountGraphqlInput
    ) -> SubAccountGraphqlType | VitaErrorGraphqlType:
        return DeleteSubAccountService(Mutation.get_session()).execute(input)

    @strawberry.mutation
    def create_journal_entry(
        self, input: JournalEntryGraphqlInput
    ) -> JournalEntryGraphqlType | VitaErrorGraphqlType:
        return CreateJournalEntryService(Mutation.get_session()).execute(input)

    @strawberry.mutation
    def update_journal_entry(
        self, input: JournalEntryGraphqlInput
    ) -> JournalEntryGraphqlType | VitaErrorGraphqlType:
        return UpdateJournalEntryService(Mutation.get_session()).execute(input)

    @strawberry.mutation
    def delete_journal_entry(
        self, input: JournalEntryGraphqlInput
    ) -> JournalEntryGraphqlType | VitaErrorGraphqlType:
        return DeleteJournalEntryService(Mutation.get_session()).execute(input)
