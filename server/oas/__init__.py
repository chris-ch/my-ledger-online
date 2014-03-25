"""
Helper functions.
"""
import datetime
import logging
_LOG = logging.getLogger('oas')

from django.contrib.auth.models import User
from django.db.models import Count

import models
import tools

_LOG.debug('initializing locator')
__locator = None

def get_locator(user=None):
    global __locator
    if user is None:
        return __locator
        
    else:
        return init_context(user)

def init_context(user):
    global __locator
    _LOG.debug('initializing context for user %s' % str(user))
    __locator = _EntityLocator(user)
    return __locator

class OasModelError(Exception):
    
    def __init__(self, message):
        self.__message = message
        
    def __str__(self):
        return 'Invalid operation: %s' % self.__message

    def get_message(self):
        return self.__message

class _EntityLocator(object):
    """
    Locating, creating and deleting persistent objects.
    """

    def __init__(self, user):
        """
        """
        _LOG.info('mapping user %s', user)
        self.user, created = User.objects.get_or_create(username=user.username)
        
    def load_currencies(self, **kwds):
        """
        """
        return models.Currency.objects.filter(**kwds).all()

    def load_account_types(self, **kwds):
        """
        """
        return models.AccountType.objects.filter(**kwds).all()

    def load_legal_entities(self, **kwds):
        """
        """
        return models.LegalEntity.objects.filter(user=self.user, **kwds).all()

    def load_legal_entity(self, **kwds):
        """
        """
        entity = models.LegalEntity.objects.get(user=self.user, **kwds)
        return entity

    def load_accounts(self, legal_entity_code, **kwds):
        """
        """
        entity = models.LegalEntity.objects.get(user=self.user, code=legal_entity_code)
        accounts = (models.Account.objects
            .filter(user=self.user, legal_entity=entity, **kwds)
            .annotate(count_entries=Count('entries'))
            )
        return accounts

    def load_internal_investments(self, legal_entity_code):
        """
        """
        return models.InternalInvestment.objects.filter(account_asset__legal_entity__code=legal_entity_code).all()

    def load_internal_investors(self, legal_entity_code):
        """
        """
        return models.InternalInvestment.objects.filter(account_liability__legal_entity__code=legal_entity_code).all()

    def load_journal_entries(self, legal_entity_code, period_name, **kwds):
        """
        """
        period = self.load_accounting_period(legal_entity_code, period_name)
        groups = models.JournalEntryGroup.objects.filter(accounting_period=period, **kwds).all()
        return groups

    def load_account(self, **kwds):
        """
        """
        return models.Account.objects.get(user=self.user, **kwds)
        
    def load_templates(self, legal_entity_code, **kwds):
        """
        """
        legal_entity = self.load_legal_entity(code=legal_entity_code)
        return models.TemplateSet.objects.filter(legal_entity=legal_entity, **kwds).all()
        
    def load_template(self, legal_entity_code, template_name, **kwds):
        """
        """
        legal_entity = self.load_legal_entity(code=legal_entity_code)
        return models.TemplateSet.objects.get(legal_entity=legal_entity, name=template_name, **kwds)

    def update_account(self, account_code,
            new_code,
            new_name,
            new_account_type_code,
            new_parent_code,
            legal_entity_code
            ):
        legal_entity = self.load_legal_entity(code=legal_entity_code)
        account = self.load_account(code=account_code, legal_entity=legal_entity)
        account.code = new_code
        account.name = new_name
        if account.account_type.code != new_account_type_code:
            new_account_type = models.AccountType.objects.get(code=new_account_type_code)
            account.update_account_type(new_account_type)
            
        if new_parent_code:
            account.parent = self.load_account(code=new_parent_code, legal_entity=legal_entity)
        
        else:
            account.parent = None
            
        account.save()
            
        return account
        
    def move_to_root(self, account_code, legal_entity_code):
        legal_entity = self.load_legal_entity(code=legal_entity_code)
        child = self.load_account(code=account_code, legal_entity=legal_entity)
        child.parent = None
        child.save()
        
    def move_account(self, account_code, target_account_code, legal_entity_code):
        legal_entity = self.load_legal_entity(code=legal_entity_code)
        child = self.load_account(code=account_code, legal_entity=legal_entity)
        parent = self.load_account(code=target_account_code, legal_entity=legal_entity)
        child.parent = parent            
        child.update_account_type(parent.account_type)
        child.save()
        
    def load_accounting_period(self, legal_entity_code, period_name=None):
        """
        """
        if period_name is None:
            period_name = '<unassigned>'
            period = self.create_accounting_period(period_name, legal_entity_code)
        
        else:
            legal_entity = _fetch_one(models.LegalEntity, code=legal_entity_code, user=self.user)
            period = _fetch_one(models.AccountingPeriod, legal_entity=legal_entity, name=period_name)
        
        return period

    def exists_legal_entity_code(self, code):
        """
        """
        legal_entity = _fetch_one_or_zero(models.LegalEntity,
                                            code=code,
                                            user=self.user)
        return legal_entity is not None

    def exists_legal_entity_name(self, name):
        """
        """
        legal_entity = _fetch_one_or_zero(models.LegalEntity,
                                            name=name,
                                            user=self.user)
        return legal_entity is not None

    def create_legal_entity(self, code, name, currency_code):
        """
        """
        tools.assert_not_none(code)
        tools.assert_not_none(name)
        tools.assert_not_empty(code)
        tools.assert_not_empty(name)
        tools.assert_no_space(code)
        currency = _fetch_one(models.Currency, code=currency_code)
        _LOG.info('creating legal entity %s, currency %s' % (code, currency.code))
        legal_entity = _fetch_one_or_zero(models.LegalEntity,
                                            code=code,
                                            user=self.user)
        if not legal_entity:
            legal_entity = models.LegalEntity(code=code, 
                                             user=self.user)
                                             
        legal_entity.name = name        
        legal_entity.currency = currency
        legal_entity.save()
        return legal_entity

    def create_currency(self, code, name):
        currency = _fetch_one_or_zero(models.Currency, code=code)
        if not currency:
            currency = models.Currency(code=code)
            
        currency.name = name
        currency.save()
        return currency

    def create_account(self, code, name, description, parent_account_code, legal_entity_code, account_type):
        """
        """
        legal_entity = _fetch_one(models.LegalEntity, code=legal_entity_code, user=self.user)
        account_type = _fetch_one(models.AccountType, code=account_type)
        account = _fetch_one_or_zero(models.Account,
                                    code=code,
                                    legal_entity=legal_entity,
                                    user=self.user
                                    )
        parent_account = _fetch_one_or_zero(models.Account,
                                    code=parent_account_code,
                                    legal_entity=legal_entity,
                                    user=self.user
                                    )
        if not account:
            account = models.Account(code=code, 
                                    legal_entity=legal_entity, 
                                    user=self.user)
            
        account.name = name
        account.description = description
        account.account_type = account_type
        account.parent = parent_account
        account.save()
        return account
        
    def create_accounts_link(self, 
                             company_code_owner, code_asset, 
                             company_code_investment, code_liability
                             ):
        
        owner = _fetch_one(models.LegalEntity, code=company_code_owner, user=self.user)
        investment = _fetch_one(models.LegalEntity, code=company_code_investment, user=self.user)
        type_asset = _fetch_one(models.AccountType, code='A')
        type_liability = _fetch_one(models.AccountType, code='L')
        account_asset = _fetch_one(models.Account, code=code_asset, legal_entity=owner, user=self.user)
        account_liability = _fetch_one(models.Account, code=code_liability, legal_entity=investment, user=self.user)
        if account_asset.account_type != type_asset:
            raise OasModelError('account %s is not an asset' % code_asset)
            
        if account_liability.account_type != type_liability:
            raise OasModelError('account %s is not a liability' % code_liability)
            
        link = _fetch_one_or_zero(models.InternalInvestment,
                                  account_asset=account_asset,
                                  account_liability=account_liability
                                  )
        if not link:
            link = models.InternalInvestment(account_asset=account_asset, account_liability=account_liability)
            link.save()
            
        return link
        
    def create_accounting_period(self, name, legal_entity_code):
        """
        """
        legal_entity = _fetch_one(models.LegalEntity, code=legal_entity_code, user=self.user)
        accounting_period = _fetch_one_or_zero(models.AccountingPeriod,
                                    name=name,
                                    legal_entity=legal_entity
                                    )
        if not accounting_period:
            accounting_period = models.AccountingPeriod(name=name, 
                                    legal_entity=legal_entity)
            accounting_period.save()
            
        return accounting_period

    def create_asset_account(self, code, name, description, parent_account_code, legal_entity_code):
        """
        """
        return self.create_account(code, name, description, parent_account_code, legal_entity_code, models.CODE_ASSETS)

    def create_liability_account(self, code, name, description, parent_account_code, legal_entity_code):
        """
        """
        return self.create_account(code, name, description, parent_account_code, legal_entity_code, models.CODE_LIABILITIES_EQUITY)

    def create_income_account(self, code, name, description, parent_account_code, legal_entity_code):
        """
        """
        return self.create_account(code, name, description, parent_account_code, legal_entity_code, models.CODE_INCOME)
        
    def create_expense_account(self, code, name, description, parent_account_code, legal_entity_code):
        """
        """
        return self.create_account(code, name, description, parent_account_code, legal_entity_code, models.CODE_EXPENSE)

    def create_operation(self, date,
                            debit_account_code,
                            credit_account_code,
                            unit_cost,
                            entity_code,
                            description='',
                            quantity=1,
                            currency_code=None,
                            ref_num=None,
                            period_name=None
                            ):
        """
        @param date: operation date (iso format: 'YYYY-MM-DD')
        @param entity_code: legal entity reference code
        @param currency_code: currency for the operation
        """
        _LOG.debug('create single operation %s' % str([date, debit_account_code, credit_account_code]))
        debit = [(debit_account_code, None, unit_cost, quantity)]
        credit = [(credit_account_code, None, unit_cost, quantity)]
        group = self.create_operation_multi(date, debit, credit, entity_code, currency_code, period_name)
        group.description = description
        group.save()
        return group
        
    def create_operation_multi(self, date,
                            list_debits,
                            list_credits,
                            entity_code,
                            currency_code=None,
                            period_name=None
                            ):
        """
        @param date: operation date (iso format: 'YYYY-MM-DD')
        @param list_debits: list of tuples (debit_account_code, description, unit_cost, quantity)
        @param list_credits: list of tuples (credit_account_code, description, unit_cost, quantity)
        @param entity_code: legal entity reference code
        @param currency_code: currency for the operation
        @param ref_num: reference number for reconciliation
        @param period_name: accounting period
        """
        entity = self.load_legal_entity(code=entity_code)        
        if currency_code is None:
            currency = entity.currency
            
        else:
            currency = _fetch_one(models.Currency, code=currency_code)
            
        (year, month, day) = map(int, date.split('-'))
        date = datetime.date(year, month, day)
        period = self.load_accounting_period(entity_code, period_name)            
        group = models.JournalEntryGroup(date=date, currency=currency, accounting_period=period)
        group.save()
        
        for code, description, unit_cost, quantity in list_debits:
            account = _fetch_one(models.Account, code=code, legal_entity=entity, user=self.user)
            entry = models.JournalEntry(
                                account=account,
                                is_debit=True,
                                quantity=quantity,
                                unit_cost=unit_cost,
                                description=description,
                                group=group
                                )
            entry.save()
            
        for code, description, unit_cost, quantity in list_credits:
            account = _fetch_one(models.Account, code=code, legal_entity=entity, user=self.user)
            entry = models.JournalEntry(
                                account=account,
                                is_debit=False,
                                quantity=quantity,
                                unit_cost=unit_cost,
                                description=description,
                                group=group
                                )
            entry.save()
            
        return group
        
    def create_templates_set(self, name, 
                    legal_entity_code,
                    currency_code=None):
        entity = self.load_legal_entity(code=legal_entity_code)        
        if currency_code is None:
            currency = entity.currency
            
        else:
            currency = _fetch_one(models.Currency, code=currency_code)
            
        templates_set = models.TemplateSet(template_currency=currency, legal_entity=entity, name=name)
        templates_set.save()
        return templates_set

    def create_template_multi(self,
                            templates_set,
                            list_debits,
                            list_credits
                            ):
        """
        @param list_debits: list of tuples (debit_account_code, description, unit_cost, quantity)
        @param list_credits: list of tuples (credit_account_code, description, unit_cost, quantity)
        @param entity_code: legal entity reference code
        """
        
        entity = templates_set.legal_entity     
        group = models.TemplateJournalEntryGroup(template_set=templates_set)
        group.save()
        
        for code, description, unit_cost, quantity in list_debits:
            _LOG.debug('processing %s' % str([code, description, unit_cost, quantity]))
            account = _fetch_one(models.Account, code=code, legal_entity=entity, user=self.user)
            entry = models.TemplateJournalEntry(
                                account=account,
                                is_debit=True,
                                quantity=quantity,
                                unit_cost=unit_cost,
                                description=description,
                                template_group=group
                                )
            entry.save()
            
        for code, description, unit_cost, quantity in list_credits:
            account = _fetch_one(models.Account, code=code, legal_entity=entity, user=self.user)
            entry = models.TemplateJournalEntry(
                                account=account,
                                is_debit=False,
                                quantity=quantity,
                                unit_cost=unit_cost,
                                description=description,
                                template_group=group
                                )
            entry.save()
            
        _LOG.debug('created %s' % str(group))
        return group

    def create_template(self, templates_set,
                            debit_account_code,
                            credit_account_code,
                            unit_cost,
                            description='',
                            quantity=1
                            ):
        """
        @param entity_code: legal entity reference code
        @param currency_code: currency for the operation
        """
        _LOG.debug('create template %s' % str([templates_set.name, debit_account_code, credit_account_code]))
        debit = [(debit_account_code, None, unit_cost, quantity)]
        credit = [(credit_account_code, None, unit_cost, quantity)]
        group = self.create_template_multi(templates_set, debit, credit)
        group.description = description
        group.save()
        return group

    def remove_account(self, account_code, legal_entity_code):
        """
        """
        legal_entity = models.LegalEntity.objects.get(code=legal_entity_code, user=self.user)
        account = models.Account.objects.get(code=account_code,
                                            legal_entity=legal_entity,
                                            user=self.user)
        #legal_entity.clean_journal_entries(account.code)
        account.delete()
        
    def delete_legal_entity(self, legal_entity_code):
        """
        """
        legal_entity = models.LegalEntity.objects.get(code=legal_entity_code, user=self.user)
        legal_entity.delete()

def _fetch_one(model_entity, **kwds):
    _LOG.debug('fetching %s with params %s' % (model_entity, kwds))
    model_entity_query = model_entity.objects
    return model_entity_query.get(**kwds)

def _fetch_one_or_zero(model_entity, **kwds):
    model_entity_query = model_entity.objects.filter(**kwds)
    entity_count = model_entity_query.count()
    entity = None
    if entity_count > 0:
        entity = _fetch_one(model_entity, **kwds)

    return entity

