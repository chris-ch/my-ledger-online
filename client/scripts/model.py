import decimal
from datetime import date


class Account(object):

    def __init__(self, code: str, name: str, account_type: str, description=None, parent_account=None):
        self.code = code
        self.name = name
        self.description = description
        self.account_type = account_type
        self.parent_account = parent_account


class LegalEntity(object):

    def __init__(self, code: str, name: str, currency: str, is_individual: bool, is_deleted: bool=False):
        self.code = code
        self.name = name
        self.currency = currency.upper()
        self.is_deleted = is_deleted
        self.is_individual = is_individual
        self.accounts = list()

    def add_account(self, account: Account):
        self.accounts.append(account)

    def find_account_by_code(self, code):
        matching_accounts = [account for account in self.accounts if account.code == code]

        if len(matching_accounts) > 1:
            raise Exception('duplicate account codes detected: {}'.format(str(matching_accounts)))

        if len(matching_accounts) == 0:
            raise Exception('undefined account code detected: {}'.format(str(code)))

        return matching_accounts[0]


class AccountingPeriod(object):
    def __init__(self, name: str, legal_entity: LegalEntity, end_date: date=None):
        self.name = name
        self.legal_entity = legal_entity
        self.end_date = end_date


class JournalEntryGroup(object):
    def __init__(self, as_of_date: date, currency: str, accounting_period: AccountingPeriod):
        self.as_of_date = as_of_date
        self.currency = currency.upper()
        self.accounting_period = accounting_period
        self.entries = list()


class JournalEntry(object):
    def __init__(self, quantity: decimal, unit_cost: decimal, is_debit: bool, account: Account, ref_num: int=None, description: str=None):
        self.quantity = quantity
        self.unit_cost = unit_cost
        self.is_debit = is_debit
        self.account = account
        self.ref_num = ref_num
        self.description = description

