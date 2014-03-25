import logging
import csv
from datetime import date
from datetime import datetime
from decimal import Decimal

import oas
import oas.tools
from oas.rpc.engine import remote
from oas.rpc.engine import remote_custom

_LOG = logging.getLogger('oas.rpc')

#
# remote procedures below
#

@remote
def get_currencies():
    locator = oas.get_locator()
    currencies = locator.load_currencies()
    return currencies

@remote
def get_account_types():
    locator = oas.get_locator()    
    account_types = locator.load_account_types()
    return account_types

@remote
def get_legal_entities():
    locator = oas.get_locator()
    legal_entities = locator.load_legal_entities()
    return legal_entities
    
@remote
def get_companies():
    locator = oas.get_locator()
    legal_entities = locator.load_legal_entities(is_individual=False)
    return legal_entities

@remote
def get_template_data(legal_entity_code, templateName):
    locator = oas.get_locator()
    template = locator.load_template(legal_entity_code, templateName)
    data = [
        [{  'is_debit': entry.is_debit,
            'account_code': entry.account.code,
            'account_type_code': entry.account.account_type.code,
            'quantity': entry.quantity,
            'unit_cost': entry.unit_cost,
            'description': entry.description
        } for entry in item.entries.all()]
                for item in template.templates.all()]
    return data

@remote
def get_templates(legal_entity_code):
    locator = oas.get_locator()
    templates = locator.load_templates(legal_entity_code)
    return templates

@remote
def get_journal_entries(legal_entity_code, period_name=None):
    locator = oas.get_locator()
    legal_entity = locator.load_legal_entity(code=legal_entity_code)
    groups = locator.load_journal_entries(legal_entity_code, period_name)
    result = list()
    for group in sorted(groups, key=lambda g: (g.date, g.ref_num)):
        debits = list()
        credits = list()
        
        for entry in group.entries.filter(is_debit=True):
            debit = { 'account': entry.account.code,
                'quantity': entry.quantity,
                'unit_cost': entry.unit_cost,
                'description': entry.description
            }
            debits.append(debit)
            
        for entry in group.entries.filter(is_debit=False):
            credit = { 'account': entry.account.code,
                'quantity': entry.quantity,
                'unit_cost': entry.unit_cost,
                'description': entry.description
            }
            credits.append(credit)
            
        row = (group, debits, credits)
        result.append(row)
        
    return result

def tree_to_dict(tree, key_transform, data_transform):
    return oas.tools.tree_to_dict(tree, 
                                  key_transform=key_transform,
                                  data_transform=data_transform
                                  )
    
def trees_to_dict(trees,
                  key_transform=lambda x: x.code,
                  data_transform=lambda x: x.name):
    outputs = list()
    for tree in trees:
        outputs.append(tree_to_dict(tree, key_transform, data_transform))
        
    return outputs
    
@remote_custom(trees_to_dict)
def get_accounts(legal_entity_code):
    locator = oas.get_locator()
    legal_entity = locator.load_legal_entity(code=legal_entity_code)
    assets_tree = legal_entity.get_asset_accounts()
    liabilities_tree = legal_entity.get_liability_accounts()
    incomes_tree = legal_entity.get_income_accounts()
    expenses_tree = legal_entity.get_expense_accounts()
    return (assets_tree, liabilities_tree, incomes_tree, expenses_tree)

@remote
def get_entries_count(legal_entity_code):
    locator = oas.get_locator()
    accounts = locator.load_accounts(legal_entity_code)
    return accounts
    
@remote
def get_internal_investments(legal_entity_code):
    locator = oas.get_locator()
    links = locator.load_internal_investments(legal_entity_code)
    results = list()
    for link in links:
        relation = (link.account_liability.legal_entity.code, link.account_liability.code)
        results.append(relation)
        
    return results

@remote
def get_internal_investors(legal_entity_code):
    locator = oas.get_locator()
    links = locator.load_internal_investors(legal_entity_code)
    results = list()
    for link in links:
        relation = (link.account_asset.legal_entity.code, link.account_asset.code)
        results.append(relation)
        
    return results

@remote
def get_children_accounts(code_parent, legal_entity_code):
    locator = oas.get_locator()
    legal_entity = locator.load_legal_entity(code=legal_entity_code)
    parent = locator.load_account(code=code_parent, legal_entity=legal_entity)
    accounts = parent.children.all()
    return accounts

#
# entity creation
#

class LegalEntityCreationFailure:
    
    def __init__(self, message):
        self.message = message
        
    def __str__(self):
        return self.message

@remote
def create_legal_entity(code, name=None, currency_code=None):
    locator = oas.get_locator()
    if not name:
        name = code
        
    if not currency_code:
        currency_code= 'USD'
        
    if locator.exists_legal_entity_code(code):
        raise LegalEntityCreationFailure('legal entity with code "%s" already exists' % code)
        
    if locator.exists_legal_entity_name(name):
        raise LegalEntityCreationFailure('legal entity with name "%s" already exists' % name)
    
    return locator.create_legal_entity(code, name, currency_code)
    
@remote
def update_account(code, new_code, new_name, new_account_type_code, new_parent_code, legal_entity_code):
    locator = oas.get_locator()
    updated_account = locator.update_account(code, new_code, new_name, new_account_type_code, new_parent_code, legal_entity_code)
    return updated_account

@remote
def remove_account(account_code, legal_entity_code):
    locator = oas.get_locator()
    locator.remove_account(account_code, legal_entity_code)

@remote
def create_asset_account(code, name, description, parent_account_code, legal_entity_code):
    locator = oas.get_locator()
    return locator.create_asset_account(code, name, description, parent_account_code, legal_entity_code)

@remote
def create_liability_account(code, name, description, parent_account_code, legal_entity_code):
    locator = oas.get_locator()
    return locator.create_liability_account(code, name, description, parent_account_code, legal_entity_code)

@remote
def create_income_account(code, name, description, parent_account_code, legal_entity_code):
    locator = oas.get_locator()
    return locator.create_income_account(code, name, description, parent_account_code, legal_entity_code)

@remote
def create_expense_account(code, name, description, parent_account_code, legal_entity_code):
    locator = oas.get_locator()
    return locator.create_expense_account(code, name, description, parent_account_code, legal_entity_code)

@remote
def create_accounts_link(owner_code, code_asset, investment_code, code_liability):
    locator = oas.get_locator()
    return locator.create_accounts_link(owner_code, code_asset, investment_code, code_liability)

@remote
def create_operation(date,
                     debit_account_code,
                     credit_account_code,
                     unit_cost,
                     entity_code,
                     description='',
                     quantity=1,
                     currency_code=None,
                     ref_num=None,
                     period_name=None):
    """
    @param date: operation date (iso format: 'YYYY-MM-DD')
    @param entity_code: legal entity reference code
    @param currency_code: currency for the operation
    """
    locator = oas.get_locator()
    locator.create_operation(date,
                     debit_account_code,
                     credit_account_code,
                     unit_cost,
                     entity_code,
                     description,
                     quantity,
                     currency_code,
                     ref_num,
                     period_name)

@remote
def move_account(code_child, code_parent, legal_entity_code):
    _LOG.debug('move_account')
    locator = oas.get_locator()
    locator.move_account(code_child, code_parent, legal_entity_code)

@remote
def move_to_root(code_child, legal_entity_code):
    _LOG.debug('move_root_account')
    locator = oas.get_locator()
    locator.move_to_root(code_child, legal_entity_code)

@remote
def move_up_account(code, legal_entity_code):
    _LOG.debug('move_up_account')
    locator = oas.get_locator()
    legal_entity = locator.load_legal_entity(code=legal_entity_code)
    account = locator.load_account(code=code, legal_entity=legal_entity)
    assert account.parent is not None, 'account %s cannot be moved upwards' % (account)
    if account.parent.parent:
        move_account(code, account.parent.parent.code, legal_entity_code)
    
    else:
        move_to_root(code, legal_entity_code)

def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]

def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')
        
@remote
def import_accounts(legal_entity_code, account_type, csv_lines):
    _LOG.debug('importing %s accounts' % account_type)
    reader = unicode_csv_reader(csv_lines)
    reader.next()
    relations = list()
    for row in reader:
        account_code = row[0]
        account_label = row[1]
        account_parent = None
        if len(row) >= 3 and row[2] != '':
            account_parent = row[2]
            relations.append((account_code, account_parent))
            
        locator = oas.get_locator()
        locator.create_account(account_code, account_label, '', legal_entity_code, account_type)
        
    for child, parent in relations:
        set_parent_account(child, parent, legal_entity_code) 

def extract_operation_data(client_data):
    return [
                client_data['accountCode'], 
                client_data.get('label', ''),
                client_data['price'],
                client_data['quantity']
           ]
@remote
def save_journal_entries(legal_entity_code, currency_code, value_date, journal_entries):
    locator = oas.get_locator()
    for journal_entry in journal_entries:
        list_debits = journal_entry['debit']
        list_credits = journal_entry['credit']
        date = value_date[:10]
                   
        locator.create_operation_multi(date,
                            map(extract_operation_data, list_debits),
                            map(extract_operation_data, list_credits),
                            legal_entity_code,
                            currency_code=currency_code,
                            period_name=None
                            )
    
@remote
def save_journal_entries_template(legal_entity_code, currency_code, template_name, journal_entries):
    locator = oas.get_locator()
    templates_set = locator.create_templates_set(
            template_name, 
            legal_entity_code,
            currency_code=currency_code)
    for journal_entry in journal_entries:
        list_debits = journal_entry['debit']
        list_credits = journal_entry['credit']
        locator.create_template_multi(
            templates_set,
            map(extract_operation_data, list_debits),
            map(extract_operation_data, list_credits)
            )
    
@remote
def import_journal_entries(legal_entity_code, csv_lines, date_fmt):
    _LOG.debug('importing journal entries for %s, date format: %s' % (legal_entity_code, date_fmt))
    reader = unicode_csv_reader(csv_lines)
    reader.next()
    def empty_as_none(value):
        return (value.strip(), None)[value.strip() == '']
        
    multi_lines = dict()
    for row_raw in reader:
        if len(row_raw) == 0:
            continue
            
        row = map(empty_as_none, row_raw)
        _LOG.debug('importing %s' % (str(row)))
        entry_date = datetime.strptime(row[0], date_fmt).date()
        date = entry_date.isoformat()
        entry_num = (int(row[1]), None)[row[1] is None]
        entry_label = row[2]
        entry_debit = row[3]
        entry_credit = row[4]
        entry_amount = Decimal(row[5])
        locator = oas.get_locator()
        if entry_debit is not None and entry_credit is not None:
            locator.create_operation(date,
                                entry_debit,
                                entry_credit,
                                entry_amount,
                                legal_entity_code,
                                description=entry_label,
                                quantity=1,
                                ref_num=entry_num
                                )
            
        else:
            if not multi_lines.has_key(entry_num):
                multi_lines[entry_num] = (list(), list(), date)
                
            if entry_debit is not None:
                deferred = (entry_debit, entry_label, entry_amount, 1)
                multi_lines[entry_num][0].append(deferred)
            
            else:
                deferred = (entry_credit, entry_label, entry_amount, 1)
                multi_lines[entry_num][1].append(deferred)
                
    for ref_num in multi_lines.keys():
        debits, credits, date = multi_lines[ref_num]
        locator.create_operation_multi(date,
                            debits,
                            credits,
                            legal_entity_code,
                            ref_num=ref_num
                            )


#
# testing
#

@remote
def subtract(minuend, subtrahend):
    return minuend - subtrahend
    
