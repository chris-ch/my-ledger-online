import csv
from datetime import datetime, date
from collections import defaultdict

from webscrapetools import keyvalue

from model import LegalEntity, Account, JournalEntryGroup, AccountingPeriod, JournalEntry
from schema import LegalEntitySchema, JournalEntrySchema, JournalEntryGroupSchema


def main():
    keyvalue.set_store_path('../../data/store')

    def scanner(entry_key: str):
        print(entry_key.strip())

    keyvalue.scan_entries(scanner)


if __name__ == '__main__':
    main()
