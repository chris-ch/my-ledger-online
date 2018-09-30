import logging

from django.db import migrations
from djangoapp import settings
from django.apps import registry


def populate_currencies(bug_apps, schema_editor):
    # BUG - use apps instead of bug_apps
    apps = registry.apps
    Currency = apps.get_model('oas', 'Currency')
    Currency.objects.create(code="USD", name="US Dollar")
    Currency.objects.create(code="GBP", name="Sterling")
    Currency.objects.create(code="CHF", name="Swiss Franc")
    Currency.objects.create(code="EUR", name="Euro")


def populate_account_types(bug_apps, schema_editor):
    # BUG - use apps instead of bug_apps
    apps = registry.apps
    AccountType = apps.get_model('oas', 'AccountType')
    AccountType.objects.create(code="A", name="Asset")
    AccountType.objects.create(code="L", name="Liability & Equity")
    AccountType.objects.create(code="I", name="Income")
    AccountType.objects.create(code="E", name="Expense")


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.RunPython(populate_currencies),
        migrations.RunPython(populate_account_types),
    ]
