import strawberry
from vita.src.model.graphql_input import (
    AccountsGraphqlInput,
    CollectJournalEntriesGraphqlInput,
    JournalEntriesGraphqlInput,
    SingleGraphqlInput,
    SubAccountsGraphqlInput,
)
from vita.src.model.graphql_type import (
    AccountGraphqlType,
    BalanceGraphqlType,
    DailyBalanceGraphqlType,
    InnerJournalEntryGraphqlType,
    JournalEntryGraphqlType,
    SubAccountGraphqlType,
)
from vita.src.service.calculate_balance_service import CalculateBalanceService
from vita.src.service.calculate_daily_balance_service import (
    CalculateDailyBalanceService,
)
from vita.src.service.collect_journal_entries_service import (
    CollectJournalEntriesService,
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

    @classmethod
    def get_session(self) -> SQLSession:
        return SQLSession(Logg())

    @strawberry.field
    def account(self, input: SingleGraphqlInput) -> AccountGraphqlType | VitaError:
        return GetAccountService(Query.get_session()).execute(input)

    @strawberry.field
    def accounts(self, input: AccountsGraphqlInput) -> list[AccountGraphqlType]:
        return GetAccountsService(Query.get_session()).execute(input)

    @strawberry.field
    def sub_account(
        self, input: SingleGraphqlInput
    ) -> SubAccountGraphqlType | VitaError:
        return GetSubAccountService(Query.get_session()).execute(input)

    @strawberry.field
    def sub_accounts(
        self, input: SubAccountsGraphqlInput
    ) -> list[SubAccountGraphqlType]:
        return GetSubAccountsService(Query.get_session()).execute(input)

    @strawberry.field
    def journal_entry(
        self, input: SingleGraphqlInput
    ) -> JournalEntryGraphqlType | VitaError:
        return GetJournalEntryService(Query.get_session()).execute(input)

    @strawberry.field
    def journal_entries(
        self, input: JournalEntriesGraphqlInput
    ) -> list[JournalEntryGraphqlType]:
        return GetJournalEntriesService(Query.get_session()).execute(input)

    @strawberry.field
    def collect_journal_entries(
        self, input: CollectJournalEntriesGraphqlInput
    ) -> list[InnerJournalEntryGraphqlType]:
        return CollectJournalEntriesService(Query.get_session()).execute(input)

    @strawberry.field
    def calculate_balance(
        self, input: CollectJournalEntriesGraphqlInput
    ) -> list[BalanceGraphqlType]:
        return CalculateBalanceService(Query.get_session()).execute(input)

    @strawberry.field
    def calculate_daily_balance(
        self, input: CollectJournalEntriesGraphqlInput
    ) -> list[DailyBalanceGraphqlType]:
        return CalculateDailyBalanceService(Query.get_session()).execute(input)
