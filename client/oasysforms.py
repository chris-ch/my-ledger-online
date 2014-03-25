# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Sep  8 2010)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.grid

import gettext
_ = gettext.gettext

###########################################################################
## Class frmOasys
###########################################################################

class frmOasys ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = _("Oasys"), pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		self.menuBar = wx.MenuBar( 0 )
		self.menuFile = wx.Menu()
		self.menuLoadPreferences = wx.MenuItem( self.menuFile, wx.ID_ANY, _("Load preferences..."), wx.EmptyString, wx.ITEM_NORMAL )
		self.menuFile.AppendItem( self.menuLoadPreferences )
		
		self.menuSavePreferences = wx.MenuItem( self.menuFile, wx.ID_ANY, _("Save preferences..."), wx.EmptyString, wx.ITEM_NORMAL )
		self.menuFile.AppendItem( self.menuSavePreferences )
		
		self.menuFile.AppendSeparator()
		
		self.menuFileNewConnection = wx.MenuItem( self.menuFile, wx.ID_ANY, _("Start Connection..."), wx.EmptyString, wx.ITEM_NORMAL )
		self.menuFile.AppendItem( self.menuFileNewConnection )
		
		self.menuFileManageConnections = wx.MenuItem( self.menuFile, wx.ID_ANY, _("Manage Connections..."), wx.EmptyString, wx.ITEM_NORMAL )
		self.menuFile.AppendItem( self.menuFileManageConnections )
		
		self.menuFile.AppendSeparator()
		
		self.menuFileExit = wx.MenuItem( self.menuFile, wx.ID_ANY, _("Exit"), wx.EmptyString, wx.ITEM_NORMAL )
		self.menuFile.AppendItem( self.menuFileExit )
		
		self.menuBar.Append( self.menuFile, _("File") ) 
		
		self.menuDirectory = wx.Menu()
		self.menuDirectoryIndividuals = wx.MenuItem( self.menuDirectory, wx.ID_ANY, _("Individuals..."), wx.EmptyString, wx.ITEM_NORMAL )
		self.menuDirectory.AppendItem( self.menuDirectoryIndividuals )
		
		self.menuDirectoryCompanies = wx.MenuItem( self.menuDirectory, wx.ID_ANY, _("Companies..."), wx.EmptyString, wx.ITEM_NORMAL )
		self.menuDirectory.AppendItem( self.menuDirectoryCompanies )
		
		self.menuBar.Append( self.menuDirectory, _("Directory") ) 
		
		self.menuTools = wx.Menu()
		self.menuToolsImport = wx.MenuItem( self.menuTools, wx.ID_ANY, _("Import accounts..."), wx.EmptyString, wx.ITEM_NORMAL )
		self.menuTools.AppendItem( self.menuToolsImport )
		
		self.menuToolsExport = wx.MenuItem( self.menuTools, wx.ID_ANY, _("Export accounts..."), wx.EmptyString, wx.ITEM_NORMAL )
		self.menuTools.AppendItem( self.menuToolsExport )
		
		self.menuTools.AppendSeparator()
		
		self.menuToolsImportEntries = wx.MenuItem( self.menuTools, wx.ID_ANY, _("Import journal entries..."), wx.EmptyString, wx.ITEM_NORMAL )
		self.menuTools.AppendItem( self.menuToolsImportEntries )
		
		self.menuToolsExportEntries = wx.MenuItem( self.menuTools, wx.ID_ANY, _("Export journal entries..."), wx.EmptyString, wx.ITEM_NORMAL )
		self.menuTools.AppendItem( self.menuToolsExportEntries )
		
		self.menuBar.Append( self.menuTools, _("Tools") ) 
		
		self.menuHelp = wx.Menu()
		self.menuHelpAbout = wx.MenuItem( self.menuHelp, wx.ID_ANY, _("About..."), wx.EmptyString, wx.ITEM_NORMAL )
		self.menuHelp.AppendItem( self.menuHelpAbout )
		
		self.menuBar.Append( self.menuHelp, _("Help") ) 
		
		self.SetMenuBar( self.menuBar )
		
		fgSizer4 = wx.FlexGridSizer( 2, 1, 0, 0 )
		fgSizer4.AddGrowableCol( 0 )
		fgSizer4.AddGrowableRow( 1 )
		fgSizer4.SetFlexibleDirection( wx.BOTH )
		fgSizer4.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_ALL )
		
		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.lblDispDataComp = wx.StaticText( self, wx.ID_ANY, _("Displaying data for company"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lblDispDataComp.Wrap( -1 )
		bSizer6.Add( self.lblDispDataComp, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		selCompaniesChoices = []
		self.selCompanies = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, selCompaniesChoices, 0 )
		self.selCompanies.SetSelection( 0 )
		bSizer6.Add( self.selCompanies, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText24 = wx.StaticText( self, wx.ID_ANY, _("Accounting period"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText24.Wrap( -1 )
		bSizer6.Add( self.m_staticText24, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		m_choice5Choices = []
		self.m_choice5 = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice5Choices, 0 )
		self.m_choice5.SetSelection( 0 )
		bSizer6.Add( self.m_choice5, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		fgSizer4.Add( bSizer6, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.nbCompany = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.pnProfile = wx.Panel( self.nbCompany, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer7 = wx.FlexGridSizer( 3, 1, 0, 0 )
		fgSizer7.SetFlexibleDirection( wx.BOTH )
		fgSizer7.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		fgSizer5 = wx.FlexGridSizer( 2, 2, 0, 0 )
		fgSizer5.SetFlexibleDirection( wx.BOTH )
		fgSizer5.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText8 = wx.StaticText( self.pnProfile, wx.ID_ANY, _("Code"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )
		fgSizer5.Add( self.m_staticText8, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.textProfileCode = wx.TextCtrl( self.pnProfile, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer5.Add( self.textProfileCode, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText9 = wx.StaticText( self.pnProfile, wx.ID_ANY, _("Name"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9.Wrap( -1 )
		fgSizer5.Add( self.m_staticText9, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.textProfileName = wx.TextCtrl( self.pnProfile, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
		fgSizer5.Add( self.textProfileName, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		fgSizer7.Add( fgSizer5, 1, wx.EXPAND, 5 )
		
		self.m_staticText10 = wx.StaticText( self.pnProfile, wx.ID_ANY, _("Description:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText10.Wrap( -1 )
		fgSizer7.Add( self.m_staticText10, 0, wx.ALL, 5 )
		
		self.textProfileDescription = wx.TextCtrl( self.pnProfile, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,-1 ), wx.HSCROLL|wx.TE_MULTILINE )
		fgSizer7.Add( self.textProfileDescription, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 5 )
		
		self.pnProfile.SetSizer( fgSizer7 )
		self.pnProfile.Layout()
		fgSizer7.Fit( self.pnProfile )
		self.nbCompany.AddPage( self.pnProfile, _("Profile"), False )
		self.pnChartOfAccounts = wx.Panel( self.nbCompany, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer24 = wx.FlexGridSizer( 1, 2, 0, 0 )
		fgSizer24.AddGrowableCol( 0 )
		fgSizer24.AddGrowableRow( 0 )
		fgSizer24.SetFlexibleDirection( wx.BOTH )
		fgSizer24.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_splitter1 = wx.SplitterWindow( self.pnChartOfAccounts, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D|wx.SP_3DSASH|wx.SP_LIVE_UPDATE )
		self.m_splitter1.SetSashGravity( 0.5 )
		self.m_splitter1.Bind( wx.EVT_IDLE, self.m_splitter1OnIdle )
		
		self.m_panel18 = wx.Panel( self.m_splitter1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer18 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_splitter2 = wx.SplitterWindow( self.m_panel18, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D|wx.SP_3DSASH|wx.SP_LIVE_UPDATE )
		self.m_splitter2.SetSashGravity( 0.5 )
		self.m_splitter2.Bind( wx.EVT_IDLE, self.m_splitter2OnIdle )
		
		self.m_panel19 = wx.Panel( self.m_splitter2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer17 = wx.FlexGridSizer( 2, 1, 0, 0 )
		fgSizer17.AddGrowableCol( 0 )
		fgSizer17.AddGrowableRow( 1 )
		fgSizer17.SetFlexibleDirection( wx.BOTH )
		fgSizer17.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText15 = wx.StaticText( self.m_panel19, wx.ID_ANY, _("Assets"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText15.Wrap( -1 )
		fgSizer17.Add( self.m_staticText15, 0, wx.ALL, 5 )
		
		self.treeAssets = wx.TreeCtrl( self.m_panel19, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE|wx.TR_HIDE_ROOT )
		self.treeAssets.SetFont( wx.Font( 7, 70, 90, 90, False, wx.EmptyString ) )
		
		self.menuAssets = wx.Menu()
		self.menuAccountCreate = wx.MenuItem( self.menuAssets, wx.ID_ANY, _("Create..."), wx.EmptyString, wx.ITEM_NORMAL )
		self.menuAssets.AppendItem( self.menuAccountCreate )
		
		self.menuAccountEdit = wx.MenuItem( self.menuAssets, wx.ID_ANY, _("Edit..."), wx.EmptyString, wx.ITEM_NORMAL )
		self.menuAssets.AppendItem( self.menuAccountEdit )
		
		self.menuAssets.AppendSeparator()
		
		self.menuAccountCut = wx.MenuItem( self.menuAssets, wx.ID_ANY, _("Cut"), wx.EmptyString, wx.ITEM_NORMAL )
		self.menuAssets.AppendItem( self.menuAccountCut )
		
		self.menuAccountPaste = wx.MenuItem( self.menuAssets, wx.ID_ANY, _("Paste"), wx.EmptyString, wx.ITEM_NORMAL )
		self.menuAssets.AppendItem( self.menuAccountPaste )
		
		self.menuAssets.AppendSeparator()
		
		self.menuAccountMoveUp = wx.MenuItem( self.menuAssets, wx.ID_ANY, _("Move up one level"), wx.EmptyString, wx.ITEM_NORMAL )
		self.menuAssets.AppendItem( self.menuAccountMoveUp )
		
		self.menuAccountMoveDown = wx.MenuItem( self.menuAssets, wx.ID_ANY, _("Move down one level..."), wx.EmptyString, wx.ITEM_NORMAL )
		self.menuAssets.AppendItem( self.menuAccountMoveDown )
		
		self.menuAssets.AppendSeparator()
		
		self.menuAccountShowEntries = wx.MenuItem( self.menuAssets, wx.ID_ANY, _("Show journal entries"), wx.EmptyString, wx.ITEM_NORMAL )
		self.menuAssets.AppendItem( self.menuAccountShowEntries )
		
		self.menuAccountInsertEntry = wx.MenuItem( self.menuAssets, wx.ID_ANY, _("Insert journal entry..."), wx.EmptyString, wx.ITEM_NORMAL )
		self.menuAssets.AppendItem( self.menuAccountInsertEntry )
		
		
		fgSizer17.Add( self.treeAssets, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_panel19.SetSizer( fgSizer17 )
		self.m_panel19.Layout()
		fgSizer17.Fit( self.m_panel19 )
		self.m_panel20 = wx.Panel( self.m_splitter2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer18 = wx.FlexGridSizer( 2, 1, 0, 0 )
		fgSizer18.AddGrowableCol( 0 )
		fgSizer18.AddGrowableRow( 1 )
		fgSizer18.SetFlexibleDirection( wx.BOTH )
		fgSizer18.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText16 = wx.StaticText( self.m_panel20, wx.ID_ANY, _("Liabilities"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText16.Wrap( -1 )
		fgSizer18.Add( self.m_staticText16, 0, wx.ALL, 5 )
		
		self.treeLiabilities = wx.TreeCtrl( self.m_panel20, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE|wx.TR_HIDE_ROOT )
		self.treeLiabilities.SetFont( wx.Font( 7, 70, 90, 90, False, wx.EmptyString ) )
		
		self.menuLiabilities = wx.Menu()
		
		fgSizer18.Add( self.treeLiabilities, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_panel20.SetSizer( fgSizer18 )
		self.m_panel20.Layout()
		fgSizer18.Fit( self.m_panel20 )
		self.m_splitter2.SplitVertically( self.m_panel19, self.m_panel20, 0 )
		bSizer18.Add( self.m_splitter2, 1, wx.EXPAND, 5 )
		
		self.m_panel18.SetSizer( bSizer18 )
		self.m_panel18.Layout()
		bSizer18.Fit( self.m_panel18 )
		self.m_panel21 = wx.Panel( self.m_splitter1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer12 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_splitter21 = wx.SplitterWindow( self.m_panel21, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D|wx.SP_3DSASH|wx.SP_LIVE_UPDATE )
		self.m_splitter21.SetSashGravity( 0.5 )
		self.m_splitter21.Bind( wx.EVT_IDLE, self.m_splitter21OnIdle )
		
		self.m_panel191 = wx.Panel( self.m_splitter21, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer171 = wx.FlexGridSizer( 2, 1, 0, 0 )
		fgSizer171.AddGrowableCol( 0 )
		fgSizer171.AddGrowableRow( 1 )
		fgSizer171.SetFlexibleDirection( wx.BOTH )
		fgSizer171.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText17 = wx.StaticText( self.m_panel191, wx.ID_ANY, _("Income Accounts"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText17.Wrap( -1 )
		fgSizer171.Add( self.m_staticText17, 0, wx.ALL, 5 )
		
		self.treeIncomeAccounts = wx.TreeCtrl( self.m_panel191, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE|wx.TR_HIDE_ROOT )
		self.treeIncomeAccounts.SetFont( wx.Font( 7, 70, 90, 90, False, wx.EmptyString ) )
		
		self.menuIncomeAccounts = wx.Menu()
		
		fgSizer171.Add( self.treeIncomeAccounts, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_panel191.SetSizer( fgSizer171 )
		self.m_panel191.Layout()
		fgSizer171.Fit( self.m_panel191 )
		self.m_panel201 = wx.Panel( self.m_splitter21, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer181 = wx.FlexGridSizer( 2, 1, 0, 0 )
		fgSizer181.AddGrowableCol( 0 )
		fgSizer181.AddGrowableRow( 1 )
		fgSizer181.SetFlexibleDirection( wx.BOTH )
		fgSizer181.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText18 = wx.StaticText( self.m_panel201, wx.ID_ANY, _("Expense Accounts"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText18.Wrap( -1 )
		fgSizer181.Add( self.m_staticText18, 0, wx.ALL, 5 )
		
		self.treeExpenseAccounts = wx.TreeCtrl( self.m_panel201, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE|wx.TR_HIDE_ROOT )
		self.treeExpenseAccounts.SetFont( wx.Font( 7, 70, 90, 90, False, wx.EmptyString ) )
		
		self.menuExpenseAccounts = wx.Menu()
		
		fgSizer181.Add( self.treeExpenseAccounts, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_panel201.SetSizer( fgSizer181 )
		self.m_panel201.Layout()
		fgSizer181.Fit( self.m_panel201 )
		self.m_splitter21.SplitVertically( self.m_panel191, self.m_panel201, 0 )
		bSizer12.Add( self.m_splitter21, 1, wx.EXPAND, 5 )
		
		self.m_panel21.SetSizer( bSizer12 )
		self.m_panel21.Layout()
		bSizer12.Fit( self.m_panel21 )
		self.m_splitter1.SplitHorizontally( self.m_panel18, self.m_panel21, 100 )
		fgSizer24.Add( self.m_splitter1, 1, wx.EXPAND, 5 )
		
		fgSizer20 = wx.FlexGridSizer( 2, 1, 0, 0 )
		fgSizer20.SetFlexibleDirection( wx.BOTH )
		fgSizer20.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		gSizer3 = wx.GridSizer( 2, 2, 0, 0 )
		
		self.m_checkBox3 = wx.CheckBox( self.pnChartOfAccounts, wx.ID_ANY, _("Assets"), wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer3.Add( self.m_checkBox3, 0, wx.ALL, 5 )
		
		self.m_checkBox4 = wx.CheckBox( self.pnChartOfAccounts, wx.ID_ANY, _("Liabilities"), wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer3.Add( self.m_checkBox4, 0, wx.ALL, 5 )
		
		self.m_checkBox5 = wx.CheckBox( self.pnChartOfAccounts, wx.ID_ANY, _("Income Accounts"), wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer3.Add( self.m_checkBox5, 0, wx.ALL, 5 )
		
		self.m_checkBox6 = wx.CheckBox( self.pnChartOfAccounts, wx.ID_ANY, _("Expense Accounts"), wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer3.Add( self.m_checkBox6, 0, wx.ALL, 5 )
		
		fgSizer20.Add( gSizer3, 1, wx.EXPAND, 5 )
		
		self.m_grid2 = wx.grid.Grid( self.pnChartOfAccounts, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		
		# Grid
		self.m_grid2.CreateGrid( 5, 4 )
		self.m_grid2.EnableEditing( True )
		self.m_grid2.EnableGridLines( True )
		self.m_grid2.EnableDragGridSize( False )
		self.m_grid2.SetMargins( 0, 0 )
		
		# Columns
		self.m_grid2.EnableDragColMove( False )
		self.m_grid2.EnableDragColSize( True )
		self.m_grid2.SetColLabelSize( 30 )
		self.m_grid2.SetColLabelValue( 0, _("Date") )
		self.m_grid2.SetColLabelValue( 1, _("Debit") )
		self.m_grid2.SetColLabelValue( 2, _("Credit") )
		self.m_grid2.SetColLabelValue( 3, _("Amount") )
		self.m_grid2.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Rows
		self.m_grid2.EnableDragRowSize( True )
		self.m_grid2.SetRowLabelSize( 0 )
		self.m_grid2.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Label Appearance
		
		# Cell Defaults
		self.m_grid2.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		fgSizer20.Add( self.m_grid2, 0, wx.ALL, 5 )
		
		fgSizer24.Add( fgSizer20, 1, wx.EXPAND, 5 )
		
		self.pnChartOfAccounts.SetSizer( fgSizer24 )
		self.pnChartOfAccounts.Layout()
		fgSizer24.Fit( self.pnChartOfAccounts )
		self.nbCompany.AddPage( self.pnChartOfAccounts, _("Chart of Accounts"), True )
		self.pnJournal = wx.Panel( self.nbCompany, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer11 = wx.FlexGridSizer( 2, 1, 0, 0 )
		fgSizer11.SetFlexibleDirection( wx.BOTH )
		fgSizer11.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self.pnJournal, wx.ID_ANY, _("New entry") ), wx.VERTICAL )
		
		fgSizer16 = wx.FlexGridSizer( 2, 6, 0, 0 )
		fgSizer16.AddGrowableCol( 2 )
		fgSizer16.SetFlexibleDirection( wx.BOTH )
		fgSizer16.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText25 = wx.StaticText( self.pnJournal, wx.ID_ANY, _("Date"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText25.Wrap( -1 )
		fgSizer16.Add( self.m_staticText25, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_BOTTOM, 5 )
		
		self.m_staticText26 = wx.StaticText( self.pnJournal, wx.ID_ANY, _("Num"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText26.Wrap( -1 )
		fgSizer16.Add( self.m_staticText26, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_BOTTOM, 5 )
		
		self.m_staticText27 = wx.StaticText( self.pnJournal, wx.ID_ANY, _("Description"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText27.Wrap( -1 )
		fgSizer16.Add( self.m_staticText27, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_BOTTOM, 5 )
		
		self.m_staticText28 = wx.StaticText( self.pnJournal, wx.ID_ANY, _("Debit"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText28.Wrap( -1 )
		fgSizer16.Add( self.m_staticText28, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_BOTTOM, 5 )
		
		self.m_staticText29 = wx.StaticText( self.pnJournal, wx.ID_ANY, _("Credit"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText29.Wrap( -1 )
		fgSizer16.Add( self.m_staticText29, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_BOTTOM, 5 )
		
		self.m_staticText30 = wx.StaticText( self.pnJournal, wx.ID_ANY, _("Amount"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText30.Wrap( -1 )
		fgSizer16.Add( self.m_staticText30, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_BOTTOM, 5 )
		
		self.m_datePicker1 = wx.DatePickerCtrl( self.pnJournal, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.DefaultSize, wx.DP_DEFAULT )
		fgSizer16.Add( self.m_datePicker1, 0, wx.ALL, 5 )
		
		self.m_textCtrl11 = wx.TextCtrl( self.pnJournal, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer16.Add( self.m_textCtrl11, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_textCtrl12 = wx.TextCtrl( self.pnJournal, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer16.Add( self.m_textCtrl12, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		m_choice6Choices = []
		self.m_choice6 = wx.Choice( self.pnJournal, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice6Choices, 0 )
		self.m_choice6.SetSelection( 0 )
		fgSizer16.Add( self.m_choice6, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		m_choice7Choices = []
		self.m_choice7 = wx.Choice( self.pnJournal, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice7Choices, 0 )
		self.m_choice7.SetSelection( 0 )
		fgSizer16.Add( self.m_choice7, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_textCtrl13 = wx.TextCtrl( self.pnJournal, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer16.Add( self.m_textCtrl13, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		sbSizer2.Add( fgSizer16, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )
		
		fgSizer11.Add( sbSizer2, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.gridEntries = wx.grid.Grid( self.pnJournal, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		
		# Grid
		self.gridEntries.CreateGrid( 10, 6 )
		self.gridEntries.EnableEditing( True )
		self.gridEntries.EnableGridLines( True )
		self.gridEntries.EnableDragGridSize( False )
		self.gridEntries.SetMargins( 0, 0 )
		
		# Columns
		self.gridEntries.SetColSize( 0, 80 )
		self.gridEntries.SetColSize( 1, 80 )
		self.gridEntries.SetColSize( 2, 164 )
		self.gridEntries.SetColSize( 3, 80 )
		self.gridEntries.SetColSize( 4, 80 )
		self.gridEntries.SetColSize( 5, 80 )
		self.gridEntries.EnableDragColMove( False )
		self.gridEntries.EnableDragColSize( True )
		self.gridEntries.SetColLabelSize( 30 )
		self.gridEntries.SetColLabelValue( 0, _("Date") )
		self.gridEntries.SetColLabelValue( 1, _("Num") )
		self.gridEntries.SetColLabelValue( 2, _("Description") )
		self.gridEntries.SetColLabelValue( 3, _("Account Debit") )
		self.gridEntries.SetColLabelValue( 4, _("Account Credit") )
		self.gridEntries.SetColLabelValue( 5, _("Amount") )
		self.gridEntries.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Rows
		self.gridEntries.EnableDragRowSize( True )
		self.gridEntries.SetRowLabelSize( 80 )
		self.gridEntries.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Label Appearance
		
		# Cell Defaults
		self.gridEntries.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		fgSizer11.Add( self.gridEntries, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.pnJournal.SetSizer( fgSizer11 )
		self.pnJournal.Layout()
		fgSizer11.Fit( self.pnJournal )
		self.nbCompany.AddPage( self.pnJournal, _("Journal"), False )
		
		fgSizer4.Add( self.nbCompany, 1, wx.EXPAND|wx.ALL, 5 )
		
		self.SetSizer( fgSizer4 )
		self.Layout()
		fgSizer4.Fit( self )
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	
	def m_splitter1OnIdle( self, event ):
		self.m_splitter1.SetSashPosition( 100 )
		self.m_splitter1.Unbind( wx.EVT_IDLE )
	
	def m_splitter2OnIdle( self, event ):
		self.m_splitter2.SetSashPosition( 0 )
		self.m_splitter2.Unbind( wx.EVT_IDLE )
	
	def m_splitter21OnIdle( self, event ):
		self.m_splitter21.SetSashPosition( 0 )
		self.m_splitter21.Unbind( wx.EVT_IDLE )
	

###########################################################################
## Class dlgConnection
###########################################################################

class dlgConnection ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _("Connection to Oasys server"), pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer5 = wx.BoxSizer( wx.VERTICAL )
		
		cmbConnectionChoiceChoices = []
		self.cmbConnectionChoice = wx.ComboBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, cmbConnectionChoiceChoices, 0 )
		self.cmbConnectionChoice.SetMinSize( wx.Size( 200,-1 ) )
		
		bSizer5.Add( self.cmbConnectionChoice, 0, wx.ALL, 5 )
		
		bSizer7 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer7.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.btnConnectCancel = wx.Button( self, wx.ID_ANY, _("Cancel"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7.Add( self.btnConnectCancel, 0, wx.ALL, 5 )
		
		self.btnConnect = wx.Button( self, wx.ID_ANY, _("Connect"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btnConnect.SetDefault() 
		bSizer7.Add( self.btnConnect, 0, wx.ALL, 5 )
		
		bSizer5.Add( bSizer7, 1, wx.EXPAND, 5 )
		
		self.SetSizer( bSizer5 )
		self.Layout()
		bSizer5.Fit( self )
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

###########################################################################
## Class dlgConnectionManager
###########################################################################

class dlgConnectionManager ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _("Managing Connections"), pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		fgSizer2 = wx.FlexGridSizer( 2, 1, 0, 0 )
		fgSizer2.SetFlexibleDirection( wx.BOTH )
		fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		fgSizer6 = wx.FlexGridSizer( 1, 2, 0, 0 )
		fgSizer6.SetFlexibleDirection( wx.BOTH )
		fgSizer6.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		listboxConnectionsChoices = []
		self.listboxConnections = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 150,300 ), listboxConnectionsChoices, wx.LB_ALWAYS_SB|wx.LB_SINGLE|wx.LB_SORT )
		self.listboxConnections.SetMinSize( wx.Size( 150,300 ) )
		
		fgSizer6.Add( self.listboxConnections, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		fgSizer7 = wx.FlexGridSizer( 2, 1, 0, 0 )
		fgSizer7.SetFlexibleDirection( wx.BOTH )
		fgSizer7.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		gSizer1 = wx.GridSizer( 6, 2, 0, 0 )
		
		self.lblConnectionName = wx.StaticText( self, wx.ID_ANY, _("Connection name"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lblConnectionName.Wrap( -1 )
		gSizer1.Add( self.lblConnectionName, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.txtConnectionName = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 150,-1 ), 0 )
		gSizer1.Add( self.txtConnectionName, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.lblConnectionUser = wx.StaticText( self, wx.ID_ANY, _("User identifier"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lblConnectionUser.Wrap( -1 )
		gSizer1.Add( self.lblConnectionUser, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.txtConnectionUser = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 150,-1 ), 0 )
		gSizer1.Add( self.txtConnectionUser, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.lblConnectionServer = wx.StaticText( self, wx.ID_ANY, _("Server name"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lblConnectionServer.Wrap( -1 )
		gSizer1.Add( self.lblConnectionServer, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.txtConnectionServerName = wx.TextCtrl( self, wx.ID_ANY, _("localhost"), wx.DefaultPosition, wx.Size( 150,-1 ), 0 )
		gSizer1.Add( self.txtConnectionServerName, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.lblConnectionPath = wx.StaticText( self, wx.ID_ANY, _("Server path"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lblConnectionPath.Wrap( -1 )
		gSizer1.Add( self.lblConnectionPath, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.txtConnectionServerPath = wx.TextCtrl( self, wx.ID_ANY, _("jsonrpc"), wx.DefaultPosition, wx.Size( 150,-1 ), 0 )
		gSizer1.Add( self.txtConnectionServerPath, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.lblConnectionPort = wx.StaticText( self, wx.ID_ANY, _("Server Port"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lblConnectionPort.Wrap( -1 )
		gSizer1.Add( self.lblConnectionPort, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.txtConnectionPort = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		gSizer1.Add( self.txtConnectionPort, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.lblConnectionMode = wx.StaticText( self, wx.ID_ANY, _("Connection Mode"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lblConnectionMode.Wrap( -1 )
		gSizer1.Add( self.lblConnectionMode, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		selConnectionModeChoices = [ _("http"), _("https") ]
		self.selConnectionMode = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, selConnectionModeChoices, 0 )
		self.selConnectionMode.SetSelection( 0 )
		gSizer1.Add( self.selConnectionMode, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		fgSizer7.Add( gSizer1, 1, wx.EXPAND, 5 )
		
		bSizer18 = wx.BoxSizer( wx.VERTICAL )
		
		self.chkConnectionAuth = wx.CheckBox( self, wx.ID_ANY, _("Server requires authentication"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.chkConnectionAuth.SetValue(True) 
		bSizer18.Add( self.chkConnectionAuth, 0, wx.ALL, 5 )
		
		self.chkConnectionDefault = wx.CheckBox( self, wx.ID_ANY, _("Use this as the default connection"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer18.Add( self.chkConnectionDefault, 0, wx.ALL, 5 )
		
		fgSizer7.Add( bSizer18, 1, wx.EXPAND, 5 )
		
		fgSizer6.Add( fgSizer7, 1, wx.EXPAND, 5 )
		
		fgSizer2.Add( fgSizer6, 1, wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
		
		bSizer7 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer7.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.btnConnectManagerClose = wx.Button( self, wx.ID_ANY, _("Close"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7.Add( self.btnConnectManagerClose, 0, wx.ALL, 5 )
		
		self.btnConnectManagerDelete = wx.Button( self, wx.ID_ANY, _("Delete"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7.Add( self.btnConnectManagerDelete, 0, wx.ALL, 5 )
		
		self.btnConnectManagerSave = wx.Button( self, wx.ID_ANY, _("Save"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btnConnectManagerSave.SetDefault() 
		bSizer7.Add( self.btnConnectManagerSave, 0, wx.ALL, 5 )
		
		fgSizer2.Add( bSizer7, 1, wx.EXPAND, 5 )
		
		self.SetSizer( fgSizer2 )
		self.Layout()
		fgSizer2.Fit( self )
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

###########################################################################
## Class dlgAccountsImport
###########################################################################

class dlgAccountsImport ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _("Importing Accounts"), pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		fgSizer13 = wx.FlexGridSizer( 3, 1, 0, 0 )
		fgSizer13.SetFlexibleDirection( wx.BOTH )
		fgSizer13.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText17 = wx.StaticText( self, wx.ID_ANY, _("Select the company to import to"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText17.Wrap( -1 )
		bSizer9.Add( self.m_staticText17, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		selCompaniesImportChoices = []
		self.selCompaniesImport = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, selCompaniesImportChoices, 0 )
		self.selCompaniesImport.SetSelection( 0 )
		bSizer9.Add( self.selCompaniesImport, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		fgSizer13.Add( bSizer9, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
		
		bSizer8 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer8.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.lblImportSelect = wx.StaticText( self, wx.ID_ANY, _("Please select the type of account you would like to import"), wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.lblImportSelect.Wrap( 200 )
		bSizer8.Add( self.lblImportSelect, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		rdAccountTypeChoices = [ _("Assets"), _("Liabilities"), _("Income Accounts"), _("Expense Accounts") ]
		self.rdAccountType = wx.RadioBox( self, wx.ID_ANY, _("Account types"), wx.DefaultPosition, wx.DefaultSize, rdAccountTypeChoices, 2, wx.RA_SPECIFY_COLS )
		self.rdAccountType.SetSelection( 0 )
		bSizer8.Add( self.rdAccountType, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.m_staticline2 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer8.Add( self.m_staticline2, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_staticText16 = wx.StaticText( self, wx.ID_ANY, _("The accounts need to be placed in a CSV file with 3 columns:\n\n- Account Identifier\n- Account Label\n- Parent Account Identifier\n\nThe first line is reserved for headers and will be ignored."), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText16.Wrap( 360 )
		bSizer8.Add( self.m_staticText16, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		fgSizer13.Add( bSizer8, 1, wx.EXPAND, 5 )
		
		m_sdbSizer1 = wx.StdDialogButtonSizer()
		self.m_sdbSizer1OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer1.AddButton( self.m_sdbSizer1OK )
		self.m_sdbSizer1Cancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer1.AddButton( self.m_sdbSizer1Cancel )
		m_sdbSizer1.Realize();
		fgSizer13.Add( m_sdbSizer1, 1, wx.EXPAND, 5 )
		
		self.SetSizer( fgSizer13 )
		self.Layout()
		fgSizer13.Fit( self )
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

###########################################################################
## Class dlgEntriesImport
###########################################################################

class dlgEntriesImport ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _("Importing Journal Entries"), pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		fgSizer13 = wx.FlexGridSizer( 4, 1, 0, 0 )
		fgSizer13.SetFlexibleDirection( wx.BOTH )
		fgSizer13.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText17 = wx.StaticText( self, wx.ID_ANY, _("Select the company to import to"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText17.Wrap( -1 )
		bSizer9.Add( self.m_staticText17, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		selCompaniesImportEntriesChoices = []
		self.selCompaniesImportEntries = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, selCompaniesImportEntriesChoices, 0 )
		self.selCompaniesImportEntries.SetSelection( 0 )
		bSizer9.Add( self.selCompaniesImportEntries, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		fgSizer13.Add( bSizer9, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
		
		bSizer8 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText16 = wx.StaticText( self, wx.ID_ANY, _("The journal entries need to be placed in a CSV file with 6 columns:\n\n- Date\n- Operation# (may be left empty)\n- Description\n- Debit Account Identifier\n- Credit Account\n- Amount\n\nThe first line is reserved for headers and will be ignored."), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText16.Wrap( 450 )
		bSizer8.Add( self.m_staticText16, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		fgSizer13.Add( bSizer8, 1, wx.EXPAND, 5 )
		
		sbSizer3 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, _("Date format") ), wx.VERTICAL )
		
		self.m_staticText22 = wx.StaticText( self, wx.ID_ANY, _("Use the following conventions for describing a \ncustom date format:\n\n%y - Year without century as a decimal number [00,99]\n%Y - Year with century as a decimal number\n%b - Locale’s abbreviated month name\n%B - Locale’s full month name\n%m - Month as a decimal number [01,12].\n%d - Day of the month as a decimal number [01,31]\n\nExample: for describing mm/dd/yyyy enter %m/%d/%Y"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText22.Wrap( -1 )
		sbSizer3.Add( self.m_staticText22, 0, wx.ALL, 5 )
		
		bSizer12 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.lblImportEntriesDateFormat = wx.StaticText( self, wx.ID_ANY, _("Please select a format"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lblImportEntriesDateFormat.Wrap( -1 )
		bSizer12.Add( self.lblImportEntriesDateFormat, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		selImportEntriesDateFormatChoices = [ _("%m/%d/%Y"), _("%m/%d/%y"), _("%Y-%m-%d"), _("%Y%m%d") ]
		self.selImportEntriesDateFormat = wx.ComboBox( self, wx.ID_ANY, _("%m/%d/%Y"), wx.DefaultPosition, wx.DefaultSize, selImportEntriesDateFormatChoices, wx.CB_DROPDOWN )
		bSizer12.Add( self.selImportEntriesDateFormat, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		sbSizer3.Add( bSizer12, 1, wx.EXPAND, 5 )
		
		fgSizer13.Add( sbSizer3, 1, wx.EXPAND, 5 )
		
		m_sdbSizer1 = wx.StdDialogButtonSizer()
		self.m_sdbSizer1OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer1.AddButton( self.m_sdbSizer1OK )
		self.m_sdbSizer1Cancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer1.AddButton( self.m_sdbSizer1Cancel )
		m_sdbSizer1.Realize();
		fgSizer13.Add( m_sdbSizer1, 1, wx.EXPAND, 5 )
		
		self.SetSizer( fgSizer13 )
		self.Layout()
		fgSizer13.Fit( self )
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

###########################################################################
## Class dlgAccountingPeriods
###########################################################################

class dlgAccountingPeriods ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _("Defining Accounting Periods"), pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		fgSizer15 = wx.FlexGridSizer( 1, 2, 0, 0 )
		fgSizer15.AddGrowableCol( 0 )
		fgSizer15.AddGrowableCol( 1 )
		fgSizer15.AddGrowableRow( 0 )
		fgSizer15.SetFlexibleDirection( wx.BOTH )
		fgSizer15.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		m_listBox2Choices = [ _("2005-2006"), _("2007"), _("2008") ]
		self.m_listBox2 = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_listBox2Choices, 0 )
		fgSizer15.Add( self.m_listBox2, 1, wx.ALL|wx.EXPAND, 5 )
		
		gSizer2 = wx.GridSizer( 2, 2, 0, 0 )
		
		self.m_staticText22 = wx.StaticText( self, wx.ID_ANY, _("MyLabel"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText22.Wrap( -1 )
		gSizer2.Add( self.m_staticText22, 0, wx.ALL, 5 )
		
		self.m_textCtrl9 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.m_textCtrl9, 0, wx.ALL, 5 )
		
		self.m_staticText23 = wx.StaticText( self, wx.ID_ANY, _("MyLabel"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText23.Wrap( -1 )
		gSizer2.Add( self.m_staticText23, 0, wx.ALL, 5 )
		
		self.m_textCtrl10 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.m_textCtrl10, 0, wx.ALL, 5 )
		
		fgSizer15.Add( gSizer2, 1, wx.EXPAND, 5 )
		
		self.SetSizer( fgSizer15 )
		self.Layout()
		fgSizer15.Fit( self )
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

