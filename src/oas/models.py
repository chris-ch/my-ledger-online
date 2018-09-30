"""
Django model for OAS.
"""
import logging

_LOG = logging.getLogger('oas.model')

from django.db import models
from django.contrib.auth.models import User

import oas.tools

CODE_ASSETS = 'A'
CODE_LIABILITIES_EQUITY = 'L'
CODE_INCOME = 'I'
CODE_EXPENSE = 'E'


#
# Custom User Model
#


#
# App model starts here
#
class AccountType(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(unique=True, max_length=3)
    name = models.CharField(unique=True, max_length=192)

    class Meta:
        db_table = u'oas_account_type'

    def __unicode__(self):
        return '%s - %s' % (self.code, self.name)


class Currency(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(unique=True, max_length=9)
    name = models.CharField(unique=True, max_length=192)

    class Meta:
        db_table = u'oas_currency'

    def __unicode__(self):
        return self.code


def build_tree(accounts):
    tree = oas.tools.SimpleTreeSet()
    for account in accounts:
        if account.parent is None:
            if not tree.has_node(account):
                tree.add_root(account)

        else:
            tree.create_parent_child(account.parent, account)

    return tree.group()


class LegalEntity(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(unique=True, max_length=96)
    name = models.CharField(unique=True, max_length=192)
    description = models.TextField(blank=True)
    is_individual = models.IntegerField(null=False, default=False, blank=True)

    user = models.ForeignKey(User, related_name='legal_entities', on_delete=models.PROTECT)
    currency = models.ForeignKey(Currency, related_name='+', null=False, blank=False, on_delete=models.PROTECT)

    class Meta:
        db_table = u'oas_legal_entity'

    def get_asset_accounts(self):
        accounts = self.accounts.filter(account_type__code=CODE_ASSETS)
        as_tree = build_tree(accounts)
        return as_tree

    def get_liability_accounts(self):
        accounts = self.accounts.filter(account_type__code=CODE_LIABILITIES_EQUITY)
        as_tree = build_tree(accounts)
        return as_tree

    def get_income_accounts(self):
        accounts = self.accounts.filter(account_type__code=CODE_INCOME)
        as_tree = build_tree(accounts)
        return as_tree

    def get_expense_accounts(self):
        accounts = self.accounts.filter(account_type__code=CODE_EXPENSE)
        as_tree = build_tree(accounts)
        return as_tree

    def clean_journal_entries(self, account_code=None):
        accounts = Account.objects.filter(legal_entity=self)
        if account_code is not None:
            accounts = accounts.filter(code=account_code)

        for account in accounts:
            JournalEntry.objects.filter(account=account).delete()

    def __unicode__(self):
        return self.code


class Account(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(unique=True, max_length=32)
    name = models.CharField(unique=True, max_length=192)
    description = models.TextField(blank=True)

    account_type = models.ForeignKey(AccountType, related_name='+', on_delete=models.PROTECT)
    legal_entity = models.ForeignKey(LegalEntity, related_name='accounts', on_delete=models.PROTECT)
    user = models.ForeignKey(User, related_name='accounts', on_delete=models.PROTECT)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.PROTECT)

    class Meta:
        db_table = u'oas_account'
        unique_together = (('legal_entity', 'code'), ('legal_entity', 'name'))

    def update_account_type(self, account_type, visited=None):
        """
        Because of redundancy in db model,
        children account types need to be updated
        """
        if visited is None:
            visited = set()

        _LOG.debug('visited: %s', visited)
        _LOG.debug('node: %s', self)
        assert self not in visited, 'tree not consistent: loop detected on %s' % (self)
        visited.add(self)
        self.account_type = account_type
        # recursive call updating children account types
        for child in self.children.all():
            child.update_account_type(account_type, visited)

    def __unicode__(self):
        return '%s - %s' % (self.code, self.name)


class InternalInvestment(models.Model):
    id = models.AutoField(primary_key=True)
    account_asset = models.ForeignKey(Account, related_name='owner_account', unique=True, on_delete=models.PROTECT)
    #account_asset = models.OneToOneField(Account, related_name='owner_account', on_delete=models.PROTECT)
    account_liability = models.ForeignKey(Account, related_name='investment_account', on_delete=models.PROTECT)

    class Meta:
        db_table = u'oas_internal_investment'
        unique_together = (('account_asset', 'account_liability'),)


class AccountingPeriod(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=128, null=False)
    till_date = models.DateTimeField(null=True)
    legal_entity = models.ForeignKey(LegalEntity, null=False, related_name='periods', on_delete=models.PROTECT)

    class Meta:
        db_table = u'oas_accounting_period'
        unique_together = (('legal_entity', 'name'), ('legal_entity', 'till_date'),)


class JournalEntryGroup(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(null=False)
    description = models.TextField(null=True)

    currency = models.ForeignKey(Currency, related_name='+', null=False, on_delete=models.PROTECT)
    accounting_period = models.ForeignKey(AccountingPeriod, related_name='+', null=False, on_delete=models.PROTECT)

    class Meta:
        db_table = u'oas_journal_entry_group'

    def __unicode__(self):
        return '<group: %s, %s>' % (self.date, self.description)


class JournalEntry(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.TextField(null=True)
    ref_num = models.IntegerField(null=True, default=False, blank=True)
    quantity = models.DecimalField(null=False, default=1.0, max_digits=22, decimal_places=6, blank=True)
    unit_cost = models.DecimalField(null=False, default=1.0, max_digits=22, decimal_places=6, blank=True)
    is_debit = models.IntegerField(null=False, default=False, blank=True)

    account = models.ForeignKey(Account, related_name='entries', null=False, on_delete=models.PROTECT)
    group = models.ForeignKey(JournalEntryGroup, related_name='entries', null=False, on_delete=models.PROTECT)

    class Meta:
        db_table = u'oas_journal_entry'

    def __unicode__(self):
        account_type = ('credit', 'debit')[self.is_debit]
        return '%s' % str([account_type, self.description, self.quantity * self.unit_cost, self.group])


class InitialAmount(models.Model):
    id = models.AutoField(primary_key=True)
    quantity = models.DecimalField(null=False, default=1.0, max_digits=22, decimal_places=6, blank=True)
    unit_cost = models.DecimalField(null=False, default=1.0, max_digits=22, decimal_places=6, blank=True)

    account = models.ForeignKey(Account, related_name='+', null=False, on_delete=models.PROTECT)
    accounting_period = models.ForeignKey(AccountingPeriod, related_name='initial_amounts', null=False,
                                          on_delete=models.PROTECT)

    class Meta:
        db_table = u'oas_initial_amount'
        unique_together = (('account', 'accounting_period'),)

    def __unicode__(self):
        return '%s' % str([self.accounting_period, self.account, self.quantity * self.unit_cost])


class TemplateSet(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=192)
    description = models.TextField(null=True)

    template_currency = models.ForeignKey(Currency, related_name='+', null=False, on_delete=models.PROTECT)
    legal_entity = models.ForeignKey(LegalEntity, null=False, related_name='templates', on_delete=models.PROTECT)

    class Meta:
        db_table = u'oas_template_name'
        unique_together = (('legal_entity', 'name'),)

    def __unicode__(self):
        return '<template set: %s>' % (self.name)


class TemplateJournalEntryGroup(models.Model):
    id = models.AutoField(primary_key=True)
    template_set = models.ForeignKey(TemplateSet, db_column='template_name_id', related_name='templates', null=False,
                                     on_delete=models.PROTECT)

    class Meta:
        db_table = u'oas_template_journal_entry_group'

    def __unicode__(self):
        return '<group template: %s>' % (self.template_set)


class TemplateJournalEntry(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.TextField(null=True)
    quantity = models.DecimalField(null=False, default=1.0, max_digits=22, decimal_places=6, blank=True)
    unit_cost = models.DecimalField(null=False, default=1.0, max_digits=22, decimal_places=6, blank=True)
    is_debit = models.IntegerField(null=False, default=False, blank=True)

    account = models.ForeignKey(Account, related_name='template_entries', null=False, on_delete=models.PROTECT)
    template_group = models.ForeignKey(TemplateJournalEntryGroup, related_name='entries', null=False,
                                       on_delete=models.PROTECT)

    class Meta:
        db_table = u'oas_template_journal_entry'

    def __unicode__(self):
        account_type = ('credit', 'debit')[self.is_debit]
        return '%s' % str([account_type, self.description, self.quantity * self.unit_cost, self.template_group])
