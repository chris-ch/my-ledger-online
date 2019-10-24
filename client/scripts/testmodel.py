import csv
from datetime import datetime, date
from collections import defaultdict

from webscrapetools import keyvalue

from model import LegalEntity, Account, JournalEntryGroup, AccountingPeriod, JournalEntry
from schema import LegalEntitySchema, JournalEntrySchema, JournalEntryGroupSchema


def load_accounts(entity: LegalEntity, accounts_file, account_type):
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
                if parent_code:
                    sub_accounts[parent_code].append(account)

                all_accounts.append(account)
                entity.add_account(account)

        for account in all_accounts:
            if account.code in sub_accounts:
                for sub_account in sub_accounts[account.code]:
                    sub_account.parent_account = account


def load_journal_entries(period: AccountingPeriod, journal_file: str):
    groups = list()
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
                    if group:
                        groups.append(group)
                    group = JournalEntryGroup(as_of_date=as_of_date, currency='chf', accounting_period=period)
                    prev_num = num

                if len(account_debit) != 0:
                    target_account = period.legal_entity.find_account_by_code(account_debit)
                    entry = JournalEntry(quantity=amount, unit_cost=1, is_debit=True, account=target_account, description=label)
                    group.entries.append(entry)

                if len(account_credit) != 0:
                    target_account = period.legal_entity.find_account_by_code(account_credit)
                    entry = JournalEntry(quantity=amount, unit_cost=1, is_debit=False, account=target_account, description=label)
                    group.entries.append(entry)

    return groups


def main():
    keyvalue.set_store_path('../../data/store')

    le1 = LegalEntity(code='le001', name='Legal Entity 1', currency='usd', is_individual=False)
    period = AccountingPeriod(name='Exercice 2011', legal_entity=le1, end_date=date(2011, 12 ,31))

    load_accounts(le1, '../data/assets.csv', 'A')
    load_accounts(le1, '../data/liabilities.csv', 'L')
    load_accounts(le1, '../data/revenues.csv', 'I')
    load_accounts(le1, '../data/expenses.csv', 'E')

    groups = load_journal_entries(period, '../data/journal-2011.csv')

    print(LegalEntitySchema().dumps(le1, indent=4))
    keyvalue.add_to_store('/'.join(['entities', le1.code]), bytes(LegalEntitySchema().dumps(le1, indent=4), encoding='utf-8'))
    print(groups[0].entries[0])
    print(JournalEntrySchema().dumps(groups[0].entries[0], indent=4))
    keyvalue.add_to_store('/'.join(['journal', le1.code, period.name]), bytes(JournalEntryGroupSchema(many=True).dumps(groups, indent=4), encoding='utf-8'))


if __name__ == '__main__':
    main()
