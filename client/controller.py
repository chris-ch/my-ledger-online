import os
import logging
import pickle
import json
from decimal import Decimal

from oasclient import jsonext
from oasclient import login_sequence

import wx

ACCOUNT_TYPE_ASSET = 'A'
ACCOUNT_TYPE_LIABILITY = 'L'
ACCOUNT_TYPE_INCOME = 'I'
ACCOUNT_TYPE_EXPENSE = 'E'

#class BasePropertyTable(wx.PyGridTableBase):
#    
#    def ResetView(self):
#        """Trim/extend the control's rows and update all values"""
#        self.getGrid().BeginBatch()
#        for current, new, delmsg, addmsg in [
#                (self.currentRows, self.GetNumberRows(), wxGRIDTABLE_NOTIFY_ROWS_DELETED, wxGRIDTABLE_NOTIFY_ROWS_APPENDED),
#                (self.currentColumns, self.GetNumberCols(), wxGRIDTABLE_NOTIFY_COLS_DELETED, wxGRIDTABLE_NOTIFY_COLS_APPENDED),
#            ]:
#            if new < current:
#                msg = wxGridTableMessage(
#                        self,
#                        delmsg,
#                        new,    # position
#                        current-new,
#                )
#                self.getGrid().ProcessTableMessage(msg)
#            elif new > current:
#                msg = wxGridTableMessage(
#                        self,
#                        addmsg,
#                        new-current
#                )
#                self.getGrid().ProcessTableMessage(msg)
#        self.UpdateValues()
#        self.getGrid().EndBatch()
#        
#        # The scroll bars aren't resized (at least on windows)
#        # Jiggling the size of the window rescales the scrollbars
#        h,w = grid.GetSize()
#        grid.SetSize((h+1, w))
#        grid.SetSize((h, w))
#        grid.ForceRefresh()
#    
#    def UpdateValues( self ):
#        """Update all displayed values"""
#        msg = wxGridTableMessage(self, wxGRIDTABLE_REQUEST_VIEW_GET_VALUES)
#        self.getGrid().ProcessTableMessage(msg)



class OasysController(object):
    
    def __init__(self, preferences):
        self.preferences = preferences
        default_prefs_name_1 = 'prefs.cfg'
        default_prefs_name_2 = 'prefs.oas'
        if os.path.isfile(default_prefs_name_1):
            logging.debug('loading preferences from %s' % str(default_prefs_name_1))
            self.load_preferences_json(default_prefs_name_1)
            
        elif os.path.isfile(default_prefs_name_2):
            logging.debug('loading preferences from %s' % str(default_prefs_name_2))
            self.load_preferences_json(default_prefs_name_2)
    
    def update_journal(self, grid, company_code):
        logging.debug('updating grid')
        grid.DeleteRows(0, grid.GetNumberRows())
        records = self.service.get_journal_entries(company_code)
        
        def fill_row(starting_row, count, entry):
            logging.debug('--> debit %s' % (str(entry)))
            num = (str(group['ref_num']), '')[group['ref_num'] is None]
            grid.SetCellValue(starting_row + count, 1, num)
            description = entry['description']
            if description is None:
                description = (group['description'], '')[group['description'] is None]
                
            grid.SetCellValue(starting_row + count, 2, description)
            amount = Decimal(entry['quantity']) * Decimal(entry['unit_cost'])
            grid.SetCellValue(starting_row + count, 5, amount.to_eng_string())
        
        for group, debits, credits in records:            
            logging.debug('loaded group %s' % (str(group)))
            
            (accounts_first, accounts_second) = (debits, credits)
            if len(debits) > len(credits):
                (accounts_first, accounts_second) = (credits, debits)
            
            starting_row = grid.GetNumberRows()
            grid.AppendRows(len(accounts_first))
            grid.SetCellValue(starting_row, 0, group['date'])
            for count, entry in enumerate(accounts_first):
                fill_row(starting_row, count, entry)
                grid.SetCellValue(starting_row + count, 3, entry['account'])
                
            starting_row = grid.GetNumberRows()
            grid.AppendRows(len(accounts_second))
            for count, entry in enumerate(accounts_second):
                fill_row(starting_row, count, entry)
                grid.SetCellValue(starting_row + count, 4, entry['account'])
    
    def load_preferences_pickle(self, path):
        del self.preferences[:]       
        loaded_prefs = pickle.load(open(path, 'rb'))
        self.preferences.extend(loaded_prefs)
        logging.debug('loaded preferences from %s' % path)
        
    def load_preferences_json(self, path):
        del self.preferences[:]       
        loaded_prefs = json.load(open(path, 'rb'))
        self.preferences.extend(loaded_prefs)
        logging.debug('loaded preferences from %s' % path)
    
    def save_preferences_pickle(self, path):
        pickle.dump(self.preferences, open(path, 'wb'))
        
    def save_preferences_json(self, path):
        json.dump(self.preferences, open(path, 'wb'), sort_keys=True, indent=4)

    def get_connections(self):
        return self.preferences
        
    def add_connection(self, connection):
        self.preferences.append(connection)

    def update_connection(self, existing_connection, connection):
        existing_connection.clear()
        existing_connection.update(connection)
    
    def remove_connection(self, name):
        connection = self.get_connection(name)
        self.preferences.remove(connection)

    def get_connection(self, name):                      
        connections_by_name = dict([(cnct['name'], cnct) 
                                    for cnct in self.get_connections()])
        connection = connections_by_name.get(name, None) 
        return connection
    
    def get_default_connection(self):
        connections = [cnct for cnct in self.get_connections()
                            if cnct['is_default']]
        if len(connections) > 0:
            return connections[0]
            
        else:
            return None
            
    def do_connect(self, connection, sel_companies, 
                   tree_assets, tree_liabilities, tree_incomes, tree_expenses, grid_journal,
                   password=None):
        user = connection['user']
        prefix = connection['connection_mode']
        server = connection['server_name']
        path = connection['server_path']
        port = connection['server_port']
        
        # TODO - figure out what to do with all this? may be good after all
        user_input_name = 'email'
        password_input_name = None
        success_url = prefix + '://' + server
        if connection['requires_auth']:
            user_input_name = 'Email'
            password_input_name = 'Passwd'
            success_url = 'http://online-acct-sys.appspot.com'
            
        login = login_sequence(user, password=password,
                        user_input_name=user_input_name, 
                        password_input_name=password_input_name, 
                        auto_register=False, login_path='/', 
                        success_url=success_url
                    )
                    
        self.service = jsonext.ServiceProxy(server, path, port=port, version='2.0')
        self.service.set_login_procedure(login)
        
        self.fill_companies(sel_companies)
        company_code = sel_companies.GetStringSelection()
        self.load_data_for_company(company_code, tree_assets, tree_liabilities, tree_incomes, tree_expenses, grid_journal)
         
    def fill_companies(self, listbox, comp_default=None):
        # updates companies in list box
        for company in self.service.get_companies():
            listbox.Insert(company['code'], 0)
            if company['code'] == comp_default:
                listbox.Select(0)
                
        if comp_default is None:
            listbox.Select(0)
            
    def load_data_for_company(self, company_code, tree_assets, tree_liabilities, tree_incomes, tree_expenses, grid_journal):
        logging.debug('loading data for company %s' % company_code)
        (assets, liabilities, income_accounts, expense_accounts) = self.service.get_accounts(company_code)
        
        def add_children(tree, accounts, parent, mapping):
            for account in accounts.keys():
                children = accounts[account]
                account_id = tree.AppendItem(parent, ' - '.join([account, mapping[account]]))
                data = wx.TreeItemData()
                data.SetData((account, mapping[account]))
                tree.SetItemData(account_id, data)
                add_children(tree, children, account_id, mapping)
                
        tree_assets.DeleteAllItems()
        tree_liabilities.DeleteAllItems()
        tree_incomes.DeleteAllItems()
        tree_expenses.DeleteAllItems()
        node = tree_assets.AddRoot('-' * 60 + ' Assets')
        add_children(tree_assets, assets[0], node, assets[1])
        node = tree_liabilities.AddRoot('-' * 60 + ' Liabilities')
        add_children(tree_liabilities, liabilities[0], node, liabilities[1])
        node = tree_incomes.AddRoot('-' * 60 + ' Income Accounts')
        add_children(tree_incomes, income_accounts[0], node, income_accounts[1])
        node = tree_expenses.AddRoot('-' * 60 + ' Expense Accounts')
        add_children(tree_expenses, expense_accounts[0], node, expense_accounts[1])
        self.update_journal(grid_journal, company_code)
                
    def import_accounts(self, company_code, csv_file_path, account_type):
        csv_lines = open(csv_file_path).readlines()
        self.service.import_accounts(company_code, account_type, csv_lines)
        
    def import_journal_entries(self, company_code, csv_file_path, date_format):
        csv_lines = open(csv_file_path).readlines()
        self.service.import_journal_entries(company_code, csv_lines, date_format)
        
