import logging
import inspect
import gettext
_ = gettext.gettext

import wx
from wx import xrc

import oasysforms

_LOG = logging.getLogger('forms')
MODE = 'XRC_OFF'
resource = None

register = list()

def load_form(name):
    mod = __import__('oasysforms', fromlist=[name])
    Klass = getattr(mod, name)
    return Klass

def create(name, parent=None, form_type='FRAME'):
    global MODE
    if MODE == 'XRC':
        from wx import xrc
        global resource
        if not resource:
            resource = xrc.XmlResource('oasysforms.xrc')
            _LOG.debug('resource file loaded')
            
        _LOG.debug('loading form %s' % str(name))
        
        form_types = dict()
        form_types['FRAME'] = ('PARENT', resource.LoadFrame)
        form_types['DIALOG'] = ('PARENT', resource.LoadDialog)
        form_types['MENU'] = ('SINGLE', resource.LoadMenu)
        
        loader_type, loader = form_types[form_type]
        if loader_type == 'PARENT':
            form = loader(parent, name)
            
        else:
            form = loader(name)
            
        return form
        
    else:
        global register
        if form_type == 'MENU':
            _LOG.debug('looking up menu %s from parent %s' % (str(name), str(parent)))
            return lookup(parent, name)
            
        else:
            Klass = load_form(name)
            form = Klass(parent)
            register.append(form)
            return form

def init_grid_entries(grid):
		grid.CreateGrid( 10, 6 )
		grid.EnableEditing( True )
		grid.EnableGridLines( True )
		grid.EnableDragGridSize( False )
		grid.SetMargins( 0, 0 )
		
		# Columns
		grid.SetColSize( 0, 80 )
		grid.SetColSize( 1, 80 )
		grid.SetColSize( 2, 164 )
		grid.SetColSize( 3, 80 )
		grid.SetColSize( 4, 80 )
		grid.SetColSize( 5, 80 )
		grid.EnableDragColMove( False )
		grid.EnableDragColSize( True )
		grid.SetColLabelSize( 30 )
		grid.SetColLabelValue( 0, _("Date") )
		grid.SetColLabelValue( 1, _("Num") )
		grid.SetColLabelValue( 2, _("Description") )
		grid.SetColLabelValue( 3, _("Account Debit") )
		grid.SetColLabelValue( 4, _("Account Credit") )
		grid.SetColLabelValue( 5, _("Amount") )
		grid.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Rows
		grid.EnableDragRowSize( True )
		grid.SetRowLabelSize( 80 )
		grid.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Label Appearance
		
		# Cell Defaults
		grid.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		
def lookup(parent, name):
    global MODE
    if MODE == 'XRC':
        from wx import xrc
        return xrc.XRCCTRL(parent, name)
        
    else:
        _LOG.debug('looking up %s parent=%s' % (name, parent))
        prop = parent.__getattribute__(name)
        return prop
      
def lookup_id(name):
    global MODE
    if MODE == 'XRC':
        return xrc.XRCID(name)
        
    else:
        global register
        for form in register:
            for prop_name, prop_value in inspect.getmembers(form):
                if not inspect.ismethod(prop_value) and not inspect.isclass(prop_value) and hasattr(prop_value, 'GetId'):
                    _LOG.info('inspecting %s' % (prop_name))
                    if name == prop_name:
                        _LOG.info('found element: %s' % str(prop_value))
                        return prop_value.GetId()
                        
        return None
    # 
    
