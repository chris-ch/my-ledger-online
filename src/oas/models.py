"""
Django model for OAS.

CREATE DATABASE IF NOT EXISTS `accounting`
  CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `accounting`;

-- at this point run manage.py syncdb
DROP TABLE IF EXISTS `oas_template_journal_entry`;
DROP TABLE IF EXISTS `oas_template_journal_entry_group`;
DROP TABLE IF EXISTS `oas_template_name`;
DROP TABLE IF EXISTS `oas_initial_amount`;
DROP TABLE IF EXISTS `oas_internal_investment`;
DROP TABLE IF EXISTS `oas_journal_entry`;
DROP TABLE IF EXISTS `oas_journal_entry_group`;
DROP TABLE IF EXISTS `oas_account`;
DROP TABLE IF EXISTS `oas_account_type`;
DROP TABLE IF EXISTS `oas_accounting_period`;
DROP TABLE IF EXISTS `oas_legal_entity`;
DROP TABLE IF EXISTS `oas_currency`;
CREATE TABLE `oas_account_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(1) NOT NULL,
  `name` varchar(64) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ;
CREATE TABLE `oas_currency` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(3) NOT NULL,
  `name` varchar(64) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ;
CREATE TABLE `oas_legal_entity` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `currency_id` int(11) NOT NULL,
  `code` varchar(32) NOT NULL,
  `name` varchar(64) NOT NULL,
  `description` longtext,
  `is_individual` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  UNIQUE KEY `name` (`name`),
  KEY `user_id` (`user_id`),
  KEY `currency_id` (`currency_id`),
  CONSTRAINT `legal_entity_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `legal_entity_ibfk_2` FOREIGN KEY (`currency_id`) REFERENCES `oas_currency` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ;
CREATE TABLE `oas_account` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(32) NOT NULL,
  `name` varchar(192) NOT NULL,
  `description` longtext,
  `account_type_id` int(11) NOT NULL,
  `legal_entity_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `parent_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY (`code`, `legal_entity_id`),
  UNIQUE KEY (`name`, `legal_entity_id`),
  KEY `account_type_id` (`account_type_id`),
  KEY `legal_entity_id` (`legal_entity_id`),
  KEY `user_id` (`user_id`),
  KEY `parent_id` (`parent_id`),
  CONSTRAINT `account_ibfk_1` FOREIGN KEY (`account_type_id`) REFERENCES `oas_account_type` (`id`),
  CONSTRAINT `account_ibfk_2` FOREIGN KEY (`legal_entity_id`) REFERENCES `oas_legal_entity` (`id`),
  CONSTRAINT `account_ibfk_3` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `account_ibfk_4` FOREIGN KEY (`parent_id`) REFERENCES `oas_account` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ;
CREATE TABLE `oas_accounting_period` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `legal_entity_id` int(11) NOT NULL,
  `till_date` datetime NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY (`name`,`legal_entity_id`),
  UNIQUE KEY (`till_date`,`legal_entity_id`),
  KEY (`legal_entity_id`),
  CONSTRAINT FOREIGN KEY (`legal_entity_id`) REFERENCES `oas_legal_entity` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 ;
CREATE TABLE `oas_journal_entry_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` datetime NOT NULL,
  `description` longtext NULL,
  `currency_id` int(11) NOT NULL,
  `accounting_period_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `currency_id` (`currency_id`),
  KEY `accounting_period_id` (`accounting_period_id`),
  CONSTRAINT FOREIGN KEY (`currency_id`) REFERENCES `oas_currency` (`id`),
  CONSTRAINT FOREIGN KEY (`accounting_period_id`) REFERENCES `oas_accounting_period` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 ;
CREATE TABLE `oas_journal_entry` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `description` longtext NULL,
  `ref_num` int(11) NULL,
  `account_id` int(11) NOT NULL,
  is_debit tinyint(1) NOT NULL,
  `quantity` decimal(20,6) NOT NULL DEFAULT '1.000000',
  `unit_cost` decimal(20,6) NOT NULL DEFAULT '1.000000',
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `account_id` (`account_id`),
  CONSTRAINT FOREIGN KEY (`account_id`) REFERENCES `oas_account` (`id`),
  CONSTRAINT FOREIGN KEY (`group_id`) REFERENCES `oas_journal_entry_group` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 ;
CREATE TABLE `oas_internal_investment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `account_asset_id` int(11) NOT NULL,
  `account_liability_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY (`account_asset_id`,`account_liability_id`),
  UNIQUE KEY (`account_asset_id`),
  KEY (`account_asset_id`),
  KEY (`account_liability_id`),
  CONSTRAINT FOREIGN KEY (`account_asset_id`) REFERENCES `oas_account` (`id`),
  CONSTRAINT FOREIGN KEY (`account_liability_id`) REFERENCES `oas_account` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ;
CREATE TABLE `oas_initial_amount` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `account_id` int(11) NOT NULL,
  `accounting_period_id` int(11) NOT NULL,
  `quantity` decimal(20,6) NOT NULL DEFAULT '1.000000',
  `unit_cost` decimal(20,6) NOT NULL DEFAULT '1.000000',
  PRIMARY KEY (`id`),
  UNIQUE KEY (`account_id`,`accounting_period_id`),
  KEY (`account_id`),
  KEY (`accounting_period_id`),
  CONSTRAINT FOREIGN KEY (`account_id`) REFERENCES `oas_account` (`id`),
  CONSTRAINT FOREIGN KEY (`accounting_period_id`) REFERENCES `oas_accounting_period` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ;
CREATE TABLE `oas_template_name` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(96) NOT NULL,
  `description` longtext,
  `template_currency_id` int(11) NOT NULL,
  `legal_entity_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT FOREIGN KEY (`template_currency_id`) REFERENCES `oas_currency` (`id`),
  CONSTRAINT FOREIGN KEY (`legal_entity_id`) REFERENCES `oas_legal_entity` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ;
CREATE TABLE `oas_template_journal_entry_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  `template_name_id` int(11) NOT NULL,
  CONSTRAINT FOREIGN KEY (`template_name_id`) REFERENCES `oas_template_name` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ;
CREATE TABLE `oas_template_journal_entry` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `description` longtext,
  `account_id` int(11) NOT NULL,
  `is_debit` tinyint(1) NOT NULL,
  `quantity` decimal(20,6) NOT NULL DEFAULT '1.000000',
  `unit_cost` decimal(20,6) NOT NULL DEFAULT '1.000000',
  `template_group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT FOREIGN KEY (`account_id`) REFERENCES `oas_account` (`id`),
  CONSTRAINT FOREIGN KEY (`template_group_id`) REFERENCES `oas_template_journal_entry_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ;
INSERT INTO oas_account_type (id,code,name) VALUES (1,'A','Asset');
INSERT INTO oas_account_type (id,code,name) VALUES (2,'L','Liability & Equity');
INSERT INTO oas_account_type (id,code,name) VALUES (3,'I','Income');
INSERT INTO oas_account_type (id,code,name) VALUES (4,'E','Expense');
INSERT INTO oas_currency (code, name) VALUES ('USD', 'US Dollar');
INSERT INTO oas_currency (code, name) VALUES ('GBP', 'Sterling');
INSERT INTO oas_currency (code, name) VALUES ('CHF', 'Swiss Franc');
INSERT INTO oas_currency (code, name) VALUES ('EUR', 'Euro');

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
