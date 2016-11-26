# -*- coding: utf-8 -*-

# Page defining dependencies

import wx

from dbr.buttons        import ButtonAdd
from dbr.buttons        import ButtonAppend
from dbr.buttons        import ButtonClear
from dbr.buttons        import ButtonRemove
from dbr.functions      import TextIsEmpty
from dbr.language       import GT
from dbr.listinput      import ListCtrlPanel
from globals.ident      import ID_APPEND
from globals.ident      import ID_DEPENDS
from globals.tooltips   import SetPageToolTips


## TODO: Doxygen
class Panel(wx.ScrolledWindow):
    def __init__(self, parent):
        wx.ScrolledWindow.__init__(self, parent, ID_DEPENDS, name=GT(u'Dependencies and Conflicts'))
        
        self.SetScrollbars(20, 20, 0, 0)
        
        txt_package = wx.StaticText(self, label=GT(u'Dependency/Conflict Package Name'), name=u'package')
        txt_version = wx.StaticText(self, label=GT(u'Version'), name=u'version')
        
        self.input_package = wx.TextCtrl(self, size=(300,25), name=u'package')
        
        opts_oper = (u'>=', u'<=', u'=', u'>>', u'<<')
        self.select_oper = wx.Choice(self, choices=opts_oper, name=u'operator')
        self.select_oper.default = 0
        self.select_oper.SetSelection(self.select_oper.default)
        
        self.input_version = wx.TextCtrl(self, name=u'version')
        
        self.input_package.SetSize((100,50))
        
        categories_panel = wx.Panel(self, style=wx.BORDER_THEME)
        
        self.default_category = u'Depends'
        
        rb_dep = wx.RadioButton(categories_panel, label=GT(u'Depends'), name=self.default_category, style=wx.RB_GROUP)
        rb_pre = wx.RadioButton(categories_panel, label=GT(u'Pre-Depends'), name=u'Pre-Depends')
        rb_rec = wx.RadioButton(categories_panel, label=GT(u'Recommends'), name=u'Recommends')
        rb_sug = wx.RadioButton(categories_panel, label=GT(u'Suggests'), name=u'Suggests')
        rb_enh = wx.RadioButton(categories_panel, label=GT(u'Enhances'), name=u'Enhances')
        rb_con = wx.RadioButton(categories_panel, label=GT(u'Conflicts'), name=u'Conflicts')
        rb_rep = wx.RadioButton(categories_panel, label=GT(u'Replaces'), name=u'Replaces')
        rb_break = wx.RadioButton(categories_panel, label=GT(u'Breaks'), name=u'Breaks')
        
        self.categories = (
            rb_dep, rb_pre, rb_rec,
            rb_sug, rb_enh, rb_con,
            rb_rep, rb_break,
        )
        
        # Buttons to add and remove dependencies from the list
        btn_add = ButtonAdd(self)
        btn_append = ButtonAppend(self)
        btn_remove = ButtonRemove(self, wx.ID_DELETE) # Change the id from wx.WXK_DELETE as workaround
        btn_clear = ButtonClear(self)
        
        # ----- List
        self.dep_area = ListCtrlPanel(self, style=wx.LC_REPORT, name=u'list')
        self.dep_area.InsertColumn(0, GT(u'Category'), width=150)
        self.dep_area.InsertColumn(1, GT(u'Package(s)'))
        
        # wx 3.0 compatibility
        if wx.MAJOR_VERSION < 3:
            self.dep_area.SetColumnWidth(100, wx.LIST_AUTOSIZE)
        
        SetPageToolTips(self)
        
        # *** Layout *** #
        
        layout_G1 = wx.GridBagSizer()
        
        # Row 1
        layout_G1.Add(txt_package, (0, 0), flag=wx.ALIGN_BOTTOM)
        layout_G1.Add(txt_version, (0, 2), flag=wx.ALIGN_BOTTOM)
        
        # Row 2
        layout_G1.Add(self.input_package, (1, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        layout_G1.Add(self.select_oper, (1, 1))
        layout_G1.Add(self.input_version, (1, 2), flag=wx.ALIGN_CENTER_VERTICAL)
        
        layout_categories = wx.GridSizer(4, 2, 5, 5)
        
        for C in self.categories:
            layout_categories.Add(C, 0)
        
        categories_panel.SetSizer(layout_categories)
        categories_panel.SetAutoLayout(True)
        categories_panel.Layout()
        
        layout_buttons = wx.BoxSizer(wx.HORIZONTAL)
        
        layout_buttons.AddMany( (
            (btn_add, 0, wx.ALIGN_CENTER_VERTICAL),
            (btn_append, 0, wx.ALIGN_CENTER_VERTICAL),
            (btn_remove, 0, wx.ALIGN_CENTER_VERTICAL),
            (btn_clear, 0, wx.ALIGN_CENTER_VERTICAL),
            ) )
        
        layout_G2 = wx.GridBagSizer(5, 5)
        layout_G2.SetCols(2)
        
        layout_G2.Add(wx.StaticText(self, label=u'Categories'), (0, 0), (1, 1), wx.ALIGN_BOTTOM)
        layout_G2.Add(categories_panel, (1, 0), flag=wx.RIGHT, border=5)
        layout_G2.Add(layout_buttons, (1, 1), flag=wx.ALIGN_BOTTOM)
        
        layout_H1 = wx.BoxSizer(wx.HORIZONTAL)
        layout_H1.Add(self.dep_area, 1, wx.EXPAND)
        
        layout_main = wx.BoxSizer(wx.VERTICAL)
        layout_main.AddSpacer(10)
        layout_main.Add(layout_G1, 0, wx.EXPAND|wx.ALL, 5)
        layout_main.Add(layout_G2, 0, wx.ALL, 5)
        layout_main.Add(layout_H1, 1, wx.EXPAND|wx.ALL, 5)
        
        self.SetAutoLayout(True)
        self.SetSizer(layout_main)
        self.Layout()
        
        # *** Events *** #
        
        wx.EVT_KEY_DOWN(self.input_package, self.SetDepends)
        wx.EVT_KEY_DOWN(self.input_version, self.SetDepends)
        
        btn_add.Bind(wx.EVT_BUTTON, self.SetDepends)
        btn_append.Bind(wx.EVT_BUTTON, self.SetDepends)
        btn_remove.Bind(wx.EVT_BUTTON, self.SetDepends)
        btn_clear.Bind(wx.EVT_BUTTON, self.SetDepends)
        
        wx.EVT_KEY_DOWN(self.dep_area, self.SetDepends)
    
    
    ## Add a category & dependency to end of list
    #  
    #  \param category
    #        \b \e unicode|str : Category label
    #  \param value
    #        \b \e unicode|str : Dependency value
    def AppendDependency(self, category, value):
        self.dep_area.AppendStringItem((category, value))
    
    
    ## TODO: Doxygen
    def GetDefaultCategory(self):
        return self.default_category
    
    
    ## TODO: Doxygen
    def ResetAllFields(self):
        for C in self.categories:
            if C.GetName() == self.default_category:
                C.SetValue(True)
                break
        
        self.input_package.Clear()
        self.select_oper.SetSelection(self.select_oper.default)
        self.input_version.Clear()
        self.dep_area.DeleteAllItems()
    
    
    ## TODO: Doxygen
    def SetDepends(self, event=None):
        try:
            key_id = event.GetKeyCode()
        
        except AttributeError:
            key_id = event.GetEventObject().GetId()
        
        addname = self.input_package.GetValue()
        oper = self.select_oper.GetStringSelection()
        ver = self.input_version.GetValue()
        addver = u'({}{})'.format(oper, ver)
            
        if key_id == wx.WXK_RETURN or key_id == wx.WXK_NUMPAD_ENTER:
            if TextIsEmpty(addname):
                return
            
            category = self.GetDefaultCategory()
            for C in self.categories:
                if C.GetValue():
                    category = C.GetName()
                    break
            
            if TextIsEmpty(ver):
                self.AppendDependency(category, addname)
            
            else:
                self.AppendDependency(category, u'{} {}'.format(addname, addver))
        
        elif key_id == ID_APPEND:
            selected_count = self.dep_area.GetSelectedItemCount()
            if not TextIsEmpty(addname) and self.dep_area.GetItemCount() and selected_count:
                listrow = None
                for X in range(selected_count):
                    if listrow == None:
                        listrow = self.dep_area.GetFirstSelected()
                    
                    else:
                        listrow = self.dep_area.GetNextSelected(listrow)
                    
                    # Get item from second column
                    colitem = self.dep_area.GetItem(listrow, 1)
                    # Get the text from that item
                    prev_text = colitem.GetText()
                    
                    if not TextIsEmpty(ver):
                        self.dep_area.SetStringItem(listrow, 1, u'{} | {} {}'.format(prev_text, addname, addver))
                    
                    else:
                        self.dep_area.SetStringItem(listrow, 1, u'{} | {}'.format(prev_text, addname))
        
        elif key_id == wx.ID_DELETE:
            self.dep_area.RemoveSelected()
        
        elif key_id == wx.ID_CLEAR:
            if self.dep_area.GetItemCount():
                confirm = wx.MessageDialog(self, GT(u'Clear all dependencies?'), GT(u'Confirm'),
                        wx.YES_NO|wx.NO_DEFAULT|wx.ICON_QUESTION)
                if confirm.ShowModal() == wx.ID_YES:
                    self.dep_area.DeleteAllItems()
        
        if event:
            event.Skip()
    
    
    ## TODO: Doxygen
    def SetFieldData(self, data):
        self.dep_area.DeleteAllItems()
        for item in data:
            item_count = len(item)
            while item_count > 1:
                item_count -= 1
                self.dep_area.InsertStringItem(0, item[0])
                self.dep_area.SetStringItem(0, 1, item[item_count])
