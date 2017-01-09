import logging
_LOG = logging.getLogger('oas.views')

import csv

from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.contrib.auth.decorators import login_required

from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

import oas
from oas import forms
from oas.tools.djangoext import render_to

@render_to('test-page.html')
def test_page(request):
    data = 'test'
    locator = oas.get_locator(request.user)
    
    entities = locator.load_legal_entities()
    current_legal_entity = entities[0]
    legal_entity_form = forms.LegalEntityForm(instance=current_legal_entity)
    tpl_params = {
      'available_legal_entities': entities,
      'legal_entity_form': legal_entity_form,
      'current_legal_entity': current_legal_entity,
      'short_legal_entity_form': forms.ShortLegalEntityForm(),
      'data': data,
    }
    return tpl_params
    
@login_required
def index(request):
    _LOG.debug('accessing as user %s' % request.user.username)
    locator = oas.get_locator(request.user)
    
    entities = locator.load_legal_entities()
    if len(entities) == 0:
        # creates a default entity
        legal_entity = locator.create_legal_entity('mybook', 'Default Book', 'USD')
        
    else:
        legal_entity = entities[0]
    
    return redirect('oas.views.display_legal_entity', legal_entity.code)

@login_required
def create_legal_entity(request):
    locator = oas.get_locator(request.user)
    entities = locator.load_legal_entities()
    legal_entity_form = forms.ShortLegalEntityForm(request.POST)
    if legal_entity_form.is_valid():
        currency_code = 'USD'
        code = legal_entity_form.cleaned_data['legal_entity_code']
        legal_entity = locator.create_legal_entity(code, code, currency_code)
        return redirect('oas.views.display_legal_entity', legal_entity.code)
        
    else:
        return redirect('oas.views.index')
    
@login_required
def delete_legal_entity(request, legal_entity_code):
    locator = oas.get_locator(request.user)
    locator.delete_legal_entity(legal_entity_code)
    return redirect('oas.views.index')
    
@login_required
@render_to('book-profile.html')
def display_legal_entity(request, legal_entity_code):
    locator = oas.get_locator(request.user)
    entities = locator.load_legal_entities()
    legal_entity = locator.load_legal_entity(code=legal_entity_code)
    legal_entity_form = forms.LegalEntityForm(instance=legal_entity)
    tpl_params = {
      'available_legal_entities': entities,
      'legal_entity_form': legal_entity_form,
      'current_legal_entity': legal_entity,
      'short_legal_entity_form': forms.ShortLegalEntityForm(),
    }
    return tpl_params
    
@login_required
@render_to('journal-entry-new.html')
def journal_entry(request, legal_entity_code):
    locator = oas.get_locator(request.user)
    entities = locator.load_legal_entities()
    legal_entity = locator.load_legal_entity(code=legal_entity_code)
    tpl_params = {
      'available_legal_entities': entities,
      'current_legal_entity': legal_entity,
      'short_legal_entity_form': forms.ShortLegalEntityForm(),
    }
    return tpl_params
    
@login_required
@render_to('accounts-manage.html')
def manage_accounts(request, legal_entity_code):
    locator = oas.get_locator(request.user)
    entities = locator.load_legal_entities()        
    legal_entity = locator.load_legal_entity(code=legal_entity_code)
    tpl_params = {
      'available_legal_entities': entities,
      'current_legal_entity': legal_entity,
      'short_legal_entity_form': forms.ShortLegalEntityForm(),
    }
    return tpl_params
    
@login_required
@render_to('accounts-import.html')
def upload_accounts_file(request, legal_entity_code):
    ignore_first_row = True
    delimiter = ','
    locator = oas.get_locator(request.user)
    entities = locator.load_legal_entities()
    legal_entity = locator.load_legal_entity(code=legal_entity_code)
    import_account_form = forms.ImportAccountsForm(request.POST, request.FILES)
    if import_account_form.is_valid():
        account_type = import_account_form.cleaned_data['account_type']
        table =  csv.reader(request.FILES['file'], delimiter=delimiter)
        if ignore_first_row:
            next(table)
            
        for row in table:
            _LOG.debug(str(row))
            account_code = row[0]
            account_label = row[1]
            account_parent_code = row[2]
            locator.create_account(account_code, account_label, '', account_parent_code, legal_entity.code, account_type.code)
            
        return redirect('oas.views.manage_accounts', legal_entity.code)
        
    else:
        tpl_params = {
          'import_account_form': import_account_form,
          'available_legal_entities': entities,
          'current_legal_entity': legal_entity,
          'short_legal_entity_form': forms.ShortLegalEntityForm(),
        }
        return tpl_params
        
    return render_to_response('upload.html', {'form': form})
    
@login_required
@render_to('accounts-import.html')
def import_accounts(request, legal_entity_code):
    locator = oas.get_locator(request.user)
    entities = locator.load_legal_entities()
    legal_entity = locator.load_legal_entity(code=legal_entity_code)
    import_account_form = forms.ImportAccountsForm()
    tpl_params = {
      'import_account_form': import_account_form,
      'available_legal_entities': entities,
      'current_legal_entity': legal_entity,
      'short_legal_entity_form': forms.ShortLegalEntityForm(),
    }
    return tpl_params
    
@login_required
@render_to('accounts-export.html')
def export_accounts(request, legal_entity_code):
    locator = oas.get_locator(request.user)
    entities = locator.load_legal_entities()
    legal_entity = locator.load_legal_entity(code=legal_entity_code)
    tpl_params = {
      'available_legal_entities': entities,
      'current_legal_entity': legal_entity,
      'short_legal_entity_form': forms.ShortLegalEntityForm(),
    }
    return tpl_params
    
@login_required
@render_to('journal.html')
def display_journal(request, legal_entity_code):
    locator = oas.get_locator(request.user)
    entities = locator.load_legal_entities()
    legal_entity = locator.load_legal_entity(code=legal_entity_code)
    tpl_params = {
      'available_legal_entities': entities,
      'current_legal_entity': legal_entity,
      'short_legal_entity_form': forms.ShortLegalEntityForm(),
    }
    return tpl_params
    
@login_required
def save_legal_entity(request, legal_entity_code):
    locator = oas.get_locator(request.user)
    legal_entity = locator.load_legal_entity(code=legal_entity_code)
    legal_entity_form = forms.LegalEntityForm(request.POST, instance=legal_entity)
    if legal_entity_form.is_valid():
        locator = oas.get_locator(request.user)
        updated_legal_entity = legal_entity_form.save()
        _LOG.info('saved %s' % updated_legal_entity)
        return redirect('oas.views.display_legal_entity', updated_legal_entity.code)
        
    else:
        messages.error(request, 'could not validate all the fields, please check the form again')
        entities = locator.load_legal_entities()
        tpl_params = {
          'available_legal_entities': entities,
          'legal_entity_form': legal_entity_form,
          'current_legal_entity': legal_entity,
          'short_legal_entity_form': forms.ShortLegalEntityForm(),
        }
        ci = RequestContext(request)
        return render_to_response('book-profile.html', tpl_params, context_instance=ci)
        
############# OLD CODE BELOW
    
@login_required
@render_to('company_profile.html')
def company_profile(request, entity_code):
    locator = oas.get_locator(request.user)
    
    entity = locator.load_legal_entity(code=entity_code)
    
    tpl_params = {
      'entity': entity,
    }
    
    return tpl_params
    
@login_required
def clean_journal(request):
    locator = oas.get_locator(request.user)
    entities = locator.load_legal_entities()
    for entity in entities:
        entity.clean_journal_entries()
        
    return redirect('oas.views.index')
    
    
@login_required
@render_to('admin_entities.html')
def admin_entities(request):
    entity_form = forms.LegalEntityForm()
    tpl_params = {
      'entity_form': entity_form,
    }
    return tpl_params
    
    
@login_required
def create_entity(request):
    entity_form = forms.LegalEntityForm(request.POST)
    if entity_form.is_valid():
        locator = oas.get_locator(request.user)
        legal_entity = entity_form.save(commit=False)
        legal_entity.user = locator.user
        legal_entity.save()
        messages.info(request, 'created entity %s' % entity_form.cleaned_data['name'])
    else:
        messages.error(request, 'could not validate all the fields, please check the form again')
        tpl_params = {
            'entity_form': entity_form,
        }
        ci = RequestContext(request)
        return render_to_response('admin_entities.html', tpl_params, context_instance=ci)
        
    return redirect('oas.views.admin_entities')
  
@login_required
def create_account(request, entity_code):
    locator = oas.get_locator(request.user)
    entity = locator.load_legal_entity(code=entity_code)
    create_account_form = forms.CreateAccountForm(request.POST, legal_entity=entity)
    if create_account_form.is_valid():
        account = create_account_form.save(commit=False)
        account.user = locator.user
        account.legal_entity = entity
        account.save()
        messages.info(request, 'created account %s - %s' % (
                       create_account_form.cleaned_data['code'], 
                       create_account_form.cleaned_data['name'])
                      )
    else:
        messages.error(request, 'could not validate all the fields, please check the form again')
        select_account_form = forms.SelectAccountForm(query_accounts=entity.accounts)
        tpl_params = {
            'select_account_form': select_account_form,
            'create_account_form': create_account_form,
            'entity': entity,
        }
        ci = RequestContext(request)
        return render_to_response('manage_accounts.html', tpl_params, context_instance=ci)
        
    return redirect('oas.views.manage_accounts', entity_code=entity_code)
  
@login_required
def save_account(request, entity_code, account_code):
    locator = oas.get_locator(request.user)
    entity = locator.load_legal_entity(code=entity_code)
    account = locator.load_account(legal_entity=entity, code=account_code)
    save_account_form = forms.SaveAccountForm(request.POST, instance=account, legal_entity=entity)
    if save_account_form.is_valid():
        account = save_account_form.save(commit=False)
        account.user = locator.user
        account.legal_entity = entity
        account.save()
        messages.info(request, 'saved account %s' % save_account_form.cleaned_data['code'])
        return redirect('oas.views.select_account', entity_code=entity.code, account_code=account.code)
        
    else:
        messages.error(request, 'could not validate all the fields, please check the form again')
        select_account_form = forms.SelectAccountForm(query_accounts=entity.accounts)
        select_account_form.initial = {'account': account}
        tpl_params = {
            'select_account_form': select_account_form,
            'save_account_form': save_account_form,
            'entity': entity,
        }
        ci = RequestContext(request)
        return render_to_response('manage_accounts.html', tpl_params, context_instance=ci)

@login_required
def select_account(request, entity_code, account_code=None):
    locator = oas.get_locator(request.user)
    entity = locator.load_legal_entity(code=entity_code)
    select_account_form = forms.SelectAccountForm(request.POST, query_accounts=entity.accounts)
    if select_account_form.is_valid():
        _LOG.debug('select form valid')
        account = select_account_form.cleaned_data['account']
        select_account_form = forms.SelectAccountForm(query_accounts=entity.accounts)            
        save_account_form = forms.SaveAccountForm(instance=account, legal_entity=entity)
        tpl_params = {       
          'entity': entity,
        }
        tpl_params['account'] = account
        tpl_params['save_account_form'] = save_account_form
        tpl_params['select_account_form'] = select_account_form
        ci = RequestContext(request)
        return render_to_response('manage_accounts.html', tpl_params, context_instance=ci)
        
    else:
        _LOG.debug('select form invalid')
        locator = oas.get_locator(request.user)
        if account_code is not None:
            account = locator.load_account(code=account_code)
            select_account_form = forms.SelectAccountForm(query_accounts=entity.accounts)
            select_account_form.initial = { 'account': account }
            save_account_form = forms.SaveAccountForm(instance=account, legal_entity=entity)
            tpl_params = {
              'entity': entity,
            }
            tpl_params['account'] = account
            tpl_params['save_account_form'] = save_account_form
            tpl_params['select_account_form'] = select_account_form
            ci = RequestContext(request)
            return render_to_response('manage_accounts.html', tpl_params, context_instance=ci)
        else:
            return redirect('oas.views.manage_accounts', entity_code=entity_code)
        
