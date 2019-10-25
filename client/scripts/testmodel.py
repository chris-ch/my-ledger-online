import csv
from datetime import datetime, date
from collections import defaultdict

from webscrapetools import keyvalue

from model import LegalEntity, Account, JournalEntryGroup, AccountingPeriod, JournalEntry
from schema import LegalEntitySchema, JournalEntrySchema, JournalEntryGroupSchema


def load_accounts(entity: LegalEntity, period_name: str, end_date: date, accounts_file, account_type):
    with open(accounts_file) as csvfile:
        accounts = csv.reader(csvfile, delimiter=',')
        first_line = True
        sub_accounts = defaultdict(list)
        all_accounts = list()
        for fields in accounts:
            if first_line: first_line = False
            else:
                code, label, parent_code, _ = fields
                account = Account(code=code, name=label, description=label, account_type=account_type)
                account.periods.append(AccountingPeriod(name=period_name, end_date=end_date))
                if parent_code:
                    sub_accounts[parent_code].append(account)

                all_accounts.append(account)
                entity.add_account(account)

        for account in all_accounts:
            if account.code in sub_accounts:
                for sub_account in sub_accounts[account.code]:
                    sub_account.parent_account = account


def load_journal_entries(entity: LegalEntity, period_name: str, journal_file: str):
    with open(journal_file) as csvfile:
        entries = csv.reader(csvfile, delimiter=',')
        first_line = True
        prev_num = None
        group = None
        for fields in entries:
            if first_line: first_line = False
            else:
                mm_dd_yyyy, num, label, account_debit, account_credit, amount = map(str.strip, fields)
                as_of_date = datetime.strptime(mm_dd_yyyy, '%m/%d/%Y').date()
                if num != prev_num:
                    group = JournalEntryGroup(as_of_date=as_of_date, currency='chf')
                    prev_num = num

                if len(account_debit) != 0:
                    entry = JournalEntry(quantity=amount, unit_cost=1, is_debit=True, entry_group=group, description=label)
                    account = entity.find_account_by_code(account_debit)
                    period = account.find_accounting_period_by_name(period_name)
                    period.entries.append(entry)

                if len(account_credit) != 0:
                    entry = JournalEntry(quantity=amount, unit_cost=1, is_debit=False, entry_group=group, description=label)
                    account = entity.find_account_by_code(account_credit)
                    period = account.find_accounting_period_by_name(period_name)
                    period.entries.append(entry)


def main():
    keyvalue.set_store_path('../../data/store')

    le1 = LegalEntity(code='le001', name='Legal Entity 1', currency='usd', is_individual=False)
    period_name =' Exercice 2011'
    end_date = date(2011, 12, 31)
    load_accounts(le1, period_name, end_date, '../data/assets.csv', 'A')
    load_accounts(le1, period_name, end_date, '../data/liabilities.csv', 'L')
    load_accounts(le1, period_name, end_date, '../data/revenues.csv', 'I')
    load_accounts(le1, period_name, end_date, '../data/expenses.csv', 'E')
    load_journal_entries(le1, period_name, '../data/journal-2011.csv')

    for account in le1.accounts:
        for period in account.periods:
            keyvalue.add_to_store('/'.join(['entities', le1.code, period.name, account.code]), bytes(JournalEntrySchema().dumps(period.entries, many=True, indent=4), encoding='utf-8'))


if __name__ == '__main__':
    main()
