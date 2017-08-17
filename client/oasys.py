import optparse
import sys
import logging
import pprint
import os.path

import wx

import formfactory
import controller
from controller import OasysController


class OasysEventHandler(object):
    def __init__(self, controller):
        self._controller = controller

    def get_controller(self):
        return self._controller


class ConnectManagerEventHandler(OasysEventHandler):
    def __init__(self, controller, parent):
        super(ConnectManagerEventHandler, self).__init__(controller)
        self.parent = parent

    def on_close(self):
        def handler(evt):
            self.parent.EndModal(wx.ID_CANCEL)

        return handler

    def select(self, connection_name):
        txt_connection_name = formfactory.lookup(self.parent, 'txtConnectionName')
        txt_user = formfactory.lookup(self.parent, 'txtConnectionUser')
        txt_server_name = formfactory.lookup(self.parent, 'txtConnectionServerName')
        txt_server_path = formfactory.lookup(self.parent, 'txtConnectionServerPath')
        txt_server_port = formfactory.lookup(self.parent, 'txtConnectionPort')
        sel_mode = formfactory.lookup(self.parent, 'selConnectionMode')
        chk_req_auth = formfactory.lookup(self.parent, 'chkConnectionAuth')
        chk_is_default = formfactory.lookup(self.parent, 'chkConnectionDefault')

        connection = self.get_controller().get_connection(connection_name)

        txt_connection_name.SetValue(connection['name'])
        txt_user.SetValue(connection['user'])
        txt_server_name.SetValue(connection['server_name'])
        txt_server_path.SetValue(connection['server_path'])
        txt_server_port.SetValue(connection['server_port'])
        sel_mode.SetStringSelection(connection['connection_mode'])
        chk_req_auth.SetValue(connection['requires_auth'])
        chk_is_default.SetValue(connection['is_default'])

    def on_connection_name_change(self):
        def handler(evt):
            connection_name = evt.GetString()
            btn_save = formfactory.lookup(self.parent, 'btnConnectManagerSave')
            if connection_name == '':
                btn_save.Disable()

            else:
                btn_save.Enable()

            btn_delete = formfactory.lookup(self.parent, 'btnConnectManagerDelete')
            if self.get_controller().get_connection(connection_name) is None:
                btn_delete.Disable()

            else:
                btn_delete.Enable()

        return handler

    def on_connection_select(self):
        def handler(evt):
            connection_name = evt.GetString()
            if connection_name == '':
                # TODO - for some reason an event is caught when the 
                # parent dialog is closed
                return

            listbox_connections = formfactory.lookup(self.parent, 'listboxConnections')
            logging.debug('selected: %s' % connection_name)
            self.select(connection_name)

        return handler

    def on_connection_delete(self):
        def handler(evt):
            txt_connection_name = formfactory.lookup(self.parent, 'txtConnectionName')
            listbox_connections = formfactory.lookup(self.parent, 'listboxConnections')

            connection_name = txt_connection_name.GetValue()
            self.get_controller().remove_connection(connection_name)
            pos = listbox_connections.FindString(connection_name)
            listbox_connections.Delete(pos)
            listbox_connections.SetSelection(0)
            self.select(listbox_connections.GetStringSelection())

        return handler

    def on_connection_save(self):
        def handler(evt):
            txt_connection_name = formfactory.lookup(self.parent, 'txtConnectionName')
            connection_name = txt_connection_name.GetValue()

            listbox_connections = formfactory.lookup(self.parent, 'listboxConnections')

            txt_user = formfactory.lookup(self.parent, 'txtConnectionUser')
            txt_server_name = formfactory.lookup(self.parent, 'txtConnectionServerName')
            txt_server_path = formfactory.lookup(self.parent, 'txtConnectionServerPath')
            txt_server_port = formfactory.lookup(self.parent, 'txtConnectionPort')
            sel_mode = formfactory.lookup(self.parent, 'selConnectionMode')
            chk_req_auth = formfactory.lookup(self.parent, 'chkConnectionAuth')
            chk_is_default = formfactory.lookup(self.parent, 'chkConnectionDefault')

            user = txt_user.GetValue()
            server_name = txt_server_name.GetValue()
            server_path = txt_server_path.GetValue()
            server_port = txt_server_port.GetValue()
            mode = sel_mode.GetString(sel_mode.GetSelection())
            req_auth = chk_req_auth.GetValue()
            is_default = chk_is_default.GetValue()

            connection = {
                'name': connection_name,
                'user': user,
                'server_name': server_name,
                'server_path': server_path,
                'server_port': server_port,
                'connection_mode': mode,
                'requires_auth': req_auth,
                'is_default': is_default,
            }

            existing_connection = self.get_controller().get_connection(connection_name)
            if not existing_connection:
                self.get_controller().add_connection(connection)
                listbox_connections.Insert(connection_name, 0)

            else:
                self.get_controller().update_connection(existing_connection, connection)

            if is_default:
                logging.debug('default connection=%s' % str(is_default))
                for other in [c for c in self.get_controller().get_connections() if c != connection]:
                    other['is_default'] = False

            pos = listbox_connections.FindString(connection_name)
            listbox_connections.Select(pos)

            btn_delete = formfactory.lookup(self.parent, 'btnConnectManagerDelete')
            btn_delete.Enable()

        return handler


class ConnectDialogEventHandler(OasysEventHandler):
    def __init__(self, controller, parent, frm_main):
        super(ConnectDialogEventHandler, self).__init__(controller)
        self.parent = parent
        self.frm_main = frm_main

    def on_cancel(self):
        def handler(evt):
            self.parent.EndModal(wx.ID_CANCEL)

        return handler

    def on_connect(self, combo_choice, list_companies):
        def handler(evt):
            connection_name = combo_choice.GetValue()
            connection = self.get_controller().get_connection(connection_name)
            password = None
            if connection['requires_auth']:
                msg = 'Please input password for user %s' % connection['user']
                dlg_pwd = wx.PasswordEntryDialog(self.parent, msg)
                if dlg_pwd.ShowModal() == wx.ID_OK:
                    password = dlg_pwd.GetValue()

                dlg_pwd.Destroy()

            tree_assets = formfactory.lookup(self.frm_main, 'treeAssets')
            tree_liabilities = formfactory.lookup(self.frm_main, 'treeLiabilities')
            tree_incomes = formfactory.lookup(self.frm_main, 'treeIncomeAccounts')
            tree_expenses = formfactory.lookup(self.frm_main, 'treeExpenseAccounts')
            grid_journal = formfactory.lookup(self.frm_main, 'gridEntries')
            self.get_controller().do_connect(connection, list_companies,
                                             tree_assets, tree_liabilities,
                                             tree_incomes, tree_expenses, grid_journal,
                                             password)

            self.parent.EndModal(wx.ID_OK)

        return handler


class MainEventHandler(OasysEventHandler):
    def __init__(self, controller, parent):
        super(MainEventHandler, self).__init__(controller)
        self.parent = parent

    def on_menu_exit(self):
        def handler(event):
            msg = 'Are your sure you want to leave the application?'
            style_yes_no = wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION
            dlg_msg = wx.MessageDialog(self.parent, msg, style=style_yes_no)
            if dlg_msg.ShowModal() == wx.ID_YES:
                logging.debug('leaving...')
                self.get_controller().save_preferences_json('prefs.cfg')
                dlg_msg.Destroy()
                sys.exit(0)

            dlg_msg.Destroy()

        return handler

    def on_menu_load_prefs(self):
        def handler(event):
            dlg = wx.FileDialog(self.parent,
                                message='Loading previously saved preferences',
                                defaultDir='',
                                defaultFile='prefs.cfg',
                                wildcard='*.cfg',
                                style=wx.FD_OPEN)
            if dlg.ShowModal() == wx.ID_OK:
                self.get_controller().load_preferences_json(dlg.GetPath())

        return handler

    def on_menu_save_prefs(self):
        def handler(event):
            dlg = wx.FileDialog(self.parent,
                                message='Saving preferences',
                                defaultDir='',
                                defaultFile='prefs.cfg',
                                wildcard='*.cfg',
                                style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
            if dlg.ShowModal() == wx.ID_OK:
                logging.debug('saving %s' % dlg.GetPath())
                self.get_controller().save_preferences_json(dlg.GetPath())

        return handler

    def on_menu_connect(self):
        def handler(evt):
            dlg = formfactory.create('dlgConnection', self.parent, form_type='DIALOG')
            btn_connect = formfactory.lookup(dlg, 'btnConnect')
            btn_cancel = formfactory.lookup(dlg, 'btnConnectCancel')
            connection_choice = formfactory.lookup(dlg, 'cmbConnectionChoice')
            for connection in self.get_controller().get_connections():
                connection_choice.Insert(connection['name'], 0)
                if connection['is_default']:
                    connection_choice.SetValue(connection['name'])

            target_list = formfactory.lookup(self.parent, 'selCompanies')
            connect_handler = ConnectDialogEventHandler(self.get_controller(), dlg, self.parent)
            btn_connect.Bind(wx.EVT_BUTTON, connect_handler.on_connect(connection_choice, target_list))
            btn_cancel.Bind(wx.EVT_BUTTON, connect_handler.on_cancel())
            dlg.ShowModal()
            dlg.Destroy()

        return handler

    def on_menu_manage_connections(self):
        def handler(evt):
            dlg = formfactory.create('dlgConnectionManager', self.parent, form_type='DIALOG')
            listbox_connections = formfactory.lookup(dlg, 'listboxConnections')
            handler = ConnectManagerEventHandler(self.get_controller(), dlg)

            for connection in self.get_controller().get_connections():
                listbox_connections.Insert(connection['name'], 0)
                if connection['is_default']:
                    listbox_connections.Select(0)
                    handler.select(connection['name'])

            btn_close = formfactory.lookup(dlg, 'btnConnectManagerClose')
            btn_close.Bind(wx.EVT_BUTTON, handler.on_close())

            btn_delete = formfactory.lookup(dlg, 'btnConnectManagerDelete')
            btn_delete.Bind(wx.EVT_BUTTON, handler.on_connection_delete())

            btn_save = formfactory.lookup(dlg, 'btnConnectManagerSave')
            btn_save.Bind(wx.EVT_BUTTON, handler.on_connection_save())

            listbox_connections = formfactory.lookup(dlg, 'listboxConnections')
            listbox_connections.Bind(wx.EVT_LISTBOX, handler.on_connection_select())

            txt_connection_name = formfactory.lookup(dlg, 'txtConnectionName')
            txt_connection_name.Bind(wx.EVT_TEXT, handler.on_connection_name_change())

            dlg.ShowModal()
            dlg.Destroy()

        return handler

    def on_menu_tools_import_accounts(self, event):
        dlg = formfactory.create('dlgAccountsImport', self.parent, form_type='DIALOG')
        sel_companies = formfactory.lookup(dlg, 'selCompaniesImport')
        sel_company_default = formfactory.lookup(self.parent, 'selCompanies')
        self.get_controller().fill_companies(sel_companies, sel_company_default.GetStringSelection())

        if dlg.ShowModal() == wx.ID_OK:
            company = sel_companies.GetStringSelection()
            rd_account_type = formfactory.lookup(dlg, 'rdAccountType')
            selection = (controller.ACCOUNT_TYPE_ASSET,
                         controller.ACCOUNT_TYPE_LIABILITY,
                         controller.ACCOUNT_TYPE_INCOME,
                         controller.ACCOUNT_TYPE_EXPENSE
                         )[rd_account_type.GetSelection()]

            dlg_csv_file = wx.FileDialog(self.parent,
                                         message='Importing %s accounts' % selection,
                                         defaultDir='',
                                         wildcard='*.csv',
                                         style=wx.FD_OPEN)

            if dlg_csv_file.ShowModal() == wx.ID_OK:
                self.get_controller().import_accounts(company, dlg_csv_file.GetPath(), selection)
                tree_assets = formfactory.lookup(self.parent, 'treeAssets')
                tree_liabilities = formfactory.lookup(self.parent, 'treeLiabilities')
                tree_incomes = formfactory.lookup(self.parent, 'treeIncomeAccounts')
                tree_expenses = formfactory.lookup(self.parent, 'treeExpenseAccounts')
                grid_journal = formfactory.lookup(self.parent, 'gridEntries')
                self.get_controller().load_data_for_company(company,
                                                            tree_assets,
                                                            tree_liabilities,
                                                            tree_incomes, tree_expenses, grid_journal)

        dlg.Destroy()

    def on_menu_tools_import_entries(self, event):
        dlg = formfactory.create('dlgEntriesImport', self.parent, form_type='DIALOG')
        sel_companies = formfactory.lookup(dlg, 'selCompaniesImportEntries')
        sel_company_default = formfactory.lookup(self.parent, 'selCompanies')
        self.get_controller().fill_companies(sel_companies, sel_company_default.GetStringSelection())

        if dlg.ShowModal() == wx.ID_OK:
            company = sel_companies.GetStringSelection()
            date_format = formfactory.lookup(dlg, 'selImportEntriesDateFormat').GetValue()
            logging.debug('date format: "%s"' % date_format)
            dlg_csv_file = wx.FileDialog(self.parent,
                                         message='Importing journal entries for %s' % company,
                                         defaultDir='',
                                         wildcard='*.csv',
                                         style=wx.FD_OPEN)

            if dlg_csv_file.ShowModal() == wx.ID_OK:
                self.get_controller().import_journal_entries(company, dlg_csv_file.GetPath(), date_format)
                tree_assets = formfactory.lookup(self.parent, 'treeAssets')
                tree_liabilities = formfactory.lookup(self.parent, 'treeLiabilities')
                tree_incomes = formfactory.lookup(self.parent, 'treeIncomeAccounts')
                tree_expenses = formfactory.lookup(self.parent, 'treeExpenseAccounts')
                grid_journal = formfactory.lookup(self.parent, 'gridEntries')
                self.get_controller().load_data_for_company(company,
                                                            tree_assets,
                                                            tree_liabilities,
                                                            tree_incomes, tree_expenses, grid_journal)

                # updates grid
                grid_journal = formfactory.lookup(self.parent, 'gridEntries')
                self.get_controller().update_journal(grid_journal, company)

        dlg.Destroy()


def oasys_main(controller, connect_default=False):
    frame = formfactory.create('frmOasys')
    eh = MainEventHandler(controller, frame)

    item_load_prefs_id = formfactory.lookup_id('menuLoadPreferences')
    frame.Bind(wx.EVT_MENU, eh.on_menu_load_prefs(), id=item_load_prefs_id)

    item_save_prefs_id = formfactory.lookup_id('menuSavePreferences')
    frame.Bind(wx.EVT_MENU, eh.on_menu_save_prefs(), id=item_save_prefs_id)

    item_exit_id = formfactory.lookup_id('menuFileExit')
    frame.Bind(wx.EVT_MENU, eh.on_menu_exit(), id=item_exit_id)
    frame.Bind(wx.EVT_CLOSE, eh.on_menu_exit())

    item_menu_connect_id = formfactory.lookup_id('menuFileNewConnection')
    frame.Bind(wx.EVT_MENU, eh.on_menu_connect(), id=item_menu_connect_id)

    item_menu_manage_connections_id = formfactory.lookup_id('menuFileManageConnections')
    eh_connection_mgr = eh.on_menu_manage_connections()
    frame.Bind(wx.EVT_MENU, eh_connection_mgr, id=item_menu_manage_connections_id)

    item_menu_tools_import_id = formfactory.lookup_id('menuToolsImport')
    frame.Bind(wx.EVT_MENU, eh.on_menu_tools_import_accounts, id=item_menu_tools_import_id)

    item_menu_tools_import_entries_id = formfactory.lookup_id('menuToolsImportEntries')
    frame.Bind(wx.EVT_MENU, eh.on_menu_tools_import_entries, id=item_menu_tools_import_entries_id)

    tree_assets = formfactory.lookup(frame, 'treeAssets')
    tree_liabilities = formfactory.lookup(frame, 'treeLiabilities')
    tree_incomes = formfactory.lookup(frame, 'treeIncomeAccounts')
    tree_expenses = formfactory.lookup(frame, 'treeExpenseAccounts')
    grid_journal = formfactory.lookup(frame, 'gridEntries')
    formfactory.init_grid_entries(grid_journal)

    def on_company_selected(event):
        company_code = event.GetString()
        controller.load_data_for_company(company_code,
                                         tree_assets,
                                         tree_liabilities,
                                         tree_incomes, tree_expenses, grid_journal)

    sel_companies = formfactory.lookup(frame, 'selCompanies')
    sel_companies.Bind(wx.EVT_CHOICE, on_company_selected)

    logging.debug('main frame bindings completed')
    frame.Show()

    def on_show_menu_asset(event):
        item_id = event.GetItem()
        value = tree_assets.GetItemData(item_id).GetData()
        logging.debug('showing context for %s' % str(value))
        logging.debug('location %s' % str(event.GetPoint()))
        tree_assets.PopupMenu(menu_asset, event.GetPoint())

    def on_show_menu_liability(event):
        item_id = event.GetItem()
        value = tree_assets.GetItemData(item_id).GetData()
        logging.debug('showing context for %s' % str(value))

    def on_show_menu_income(event):
        item_id = event.GetItem()
        value = tree_assets.GetItemData(item_id).GetData()
        logging.debug('showing context for %s' % str(value))

    def on_show_menu_expense(event):
        item_id = event.GetItem()
        value = tree_assets.GetItemData(item_id).GetData()
        logging.debug('showing context for %s' % str(value))

    menu_asset = formfactory.create('menuAssets', parent=frame, form_type='MENU')
    logging.debug('fetched menu %s' % (str(menu_asset)))

    tree_assets.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, on_show_menu_asset)
    tree_liabilities.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, on_show_menu_liability)
    tree_incomes.Bind(wx.EVT_TREE_ITEM_MENU, on_show_menu_income)
    tree_expenses.Bind(wx.EVT_TREE_ITEM_MENU, on_show_menu_expense)

    if connect_default:
        logging.debug('auto connect')
        connection = controller.get_default_connection()
        if connection:
            controller.do_connect(connection, sel_companies,
                                  tree_assets, tree_liabilities,
                                  tree_incomes, tree_expenses, grid_journal)


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
    ch.setFormatter(formatter)
    logging.getLogger().addHandler(ch)

    parser = optparse.OptionParser()
    parser.add_option('-c', '--connect-default', action='store_true',
                      help='connects right away using the default if it is defined')
    (options, args) = parser.parse_args()

    app = wx.App(redirect=True)
    try:
        preferences = list()
        ctrl = OasysController(preferences)
        oasys_main(ctrl, options.connect_default)

    except:
        import traceback

        exc_type, exc_value, exc_tb = sys.exc_info()
        tb = traceback.format_exception(exc_type, exc_value, exc_tb)
        logging.error('an error occured: %s' % (''.join(tb)))

    app.MainLoop()
