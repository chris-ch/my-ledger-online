from django import forms
from django.core.exceptions import ValidationError

import oas
from oas import models

import logging

_LOG = logging.getLogger('oas.forms')


class ShortLegalEntityForm(forms.Form):
    legal_entity_code = forms.CharField(label='Short name',
                                        widget=forms.TextInput(attrs={
                                            'placeholder': 'Please enter a short name (no spaces allowed)',
                                            'ng-model': 'legal_entity_code',
                                        }))


class LegalEntityForm(forms.ModelForm):
    class Meta:
        model = models.LegalEntity
        fields = ['name', 'code', 'currency', 'description']
        exclude = ('user', 'is_individual', 'id')

    def __init__(self, *args, **kwargs):
        super(LegalEntityForm, self).__init__(*args, **kwargs)
        self.label_suffix = ''
        self.fields['currency'].empty_label = None
        self.fields['name'].label = 'Name'
        self.fields['code'].label = 'Short name'
        self.fields['currency'].label = 'Reporting currency'


class AccountTypeModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, account_type):
        return '%s' % account_type.name


class ImportAccountsForm(forms.Form):
    file = forms.FileField(label='Select a CSV file')
    account_type = AccountTypeModelChoiceField(
        queryset=models.AccountType.objects.all(),
        empty_label=None)
    has_header = forms.BooleanField(label='Ignore first line (header)')


##################### OLD FORMS BELOW

class SelectAccountForm(forms.Form):
    account = forms.ModelChoiceField(queryset=models.Account.objects.none())

    def __init__(self, *args, **kwargs):
        query_accounts = kwargs.pop('query_accounts', None)
        super(SelectAccountForm, self).__init__(*args, **kwargs)
        self.fields['account'].queryset = query_accounts


class CreateAccountForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.legal_entity = kwargs.pop('legal_entity', None)
        super(CreateAccountForm, self).__init__(*args, **kwargs)
        self.fields['parent'].queryset = self.legal_entity.accounts

    class Meta:
        model = models.Account
        exclude = ('user', 'legal_entity', 'id',)
        widgets = {
            'description': forms.Textarea(attrs={'cols': 40, 'rows': 3}),
        }


class SaveAccountForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.legal_entity = kwargs.pop('legal_entity', None)
        super(SaveAccountForm, self).__init__(*args, **kwargs)
        self.fields['parent'].queryset = self.legal_entity.accounts

    class Meta:
        model = models.Account
        exclude = ('user', 'legal_entity', 'id',)
        widgets = {
            'description': forms.Textarea(attrs={'cols': 40, 'rows': 3}),
            # 'code': forms.TextInput(attrs={'readonly': True}),
        }
