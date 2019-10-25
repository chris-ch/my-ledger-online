import decimal
import uuid
from collections import Iterable
from datetime import date


class AccountingPeriod(object):
    def __init__(self, name: str, end_date: date=None, entries=None):
        self.name = name
        self.end_date = end_date
        self.entries = entries if entries else list()


class Account(object):

    def __init__(self, code: str, name: str, account_type: str, periods=None, description=None, parent_account=None):
        self.code = code
        self.name = name
        self.account_type = account_type
        self.periods = periods if periods else list()
        self.description = description
        self.parent_account = parent_account

    def find_accounting_period_by_name(self, period_name: str) -> AccountingPeriod:
        matching_periods = [period for period in self.periods if period.name == period_name]

        if len(matching_periods) > 1:
            raise Exception('duplicate accounting period names detected: {}'.format(str(matching_periods)))

        if len(matching_periods) == 0:
            raise Exception('undefined accounting period name detected: {}'.format(str(period_name)))

        return matching_periods[0]


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

    def find_account_by_code(self, code: str) -> Account:
        matching_accounts = [account for account in self.accounts if account.code == code]

        if len(matching_accounts) > 1:
            raise Exception('duplicate account codes detected: {}'.format(str(matching_accounts)))

        if len(matching_accounts) == 0:
            raise Exception('undefined account code detected: {}'.format(str(code)))

        return matching_accounts[0]


class JournalEntryGroup(object):
    def __init__(self, as_of_date: date, currency: str, id=None, description: str=None):
        self.id = id if id else uuid.uuid1()
        self.as_of_date = as_of_date
        self.description = description
        self.currency = currency.upper()


class JournalEntry(object):
    def __init__(self, quantity: decimal, unit_cost: decimal, is_debit: bool, entry_group: JournalEntryGroup, ref_num: int=None, description: str=None):
        self.quantity = quantity
        self.unit_cost = unit_cost
        self.is_debit = is_debit
        self.entry_group = entry_group
        self.ref_num = ref_num
        self.description = description
