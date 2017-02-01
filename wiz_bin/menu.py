# -*- coding: utf-8 -*-

## \package wiz_bin.menu

# MIT licensing
# See: docs/LICENSE.txt


import os, shutil, wx

from dbr.language           import GT
from dbr.log                import DebugEnabled
from dbr.log                import Logger
from globals.fileio         import ReadFile
from globals.fileio         import WriteFile
from globals.ident          import chkid
from globals.ident          import inputid
from globals.ident          import pgid
from globals.strings        import GS
from globals.strings        import TextIsEmpty
from globals.tooltips       import SetPageToolTips
from globals.wizardhelper   import GetMainWindow
from input.list             import ListCtrl
from input.select           import Choice
from input.select           import ComboBox
from input.text             import TextArea
from input.text             import TextAreaPanel
from input.toggle           import CheckBox
from ui.button              import ButtonAdd
from ui.button              import ButtonBrowse64
from ui.button              import ButtonClear
from ui.button              import ButtonPreview64
from ui.button              import ButtonRemove
from ui.button              import ButtonSave64
from ui.dialog              import ConfirmationDialog
from ui.dialog              import ShowDialog
from ui.dialog              import ShowErrorDialog
from ui.layout              import BoxSizer
from ui.textpreview         import TextPreview
from ui.wizard              import WizardPage


## Page for creating a system menu launcher
class Panel(WizardPage):
    def __init__(self, parent):
        WizardPage.__init__(self, parent, pgid.MENU) #, name=GT(u'Menu Launcher'))
        
        ## Override default label
        self.label = GT(u'Menu Launcher')
        
        self.opts_button = []
        self.opts_input = []
        self.opts_choice = []
        self.opts_list = []
        
        self.labels = []
        
        # --- Buttons to open/preview/save .desktop file
        btn_open = ButtonBrowse64(self)
        btn_open.SetName(u'open')
        
        btn_save = ButtonSave64(self)
        btn_save.SetName(u'export')
        self.opts_button.append(btn_save)
        
        btn_preview = ButtonPreview64(self)
        btn_preview.SetName(u'preview')
        self.opts_button.append(btn_preview)
        
        # --- CHECKBOX
        self.chk_enable = CheckBox(self, label=GT(u'Create system menu launcher'))
        
        # --- Custom output filename
        self.txt_filename = wx.StaticText(self, label=GT(u'Filename'), name=u'filename')
        self.ti_filename = TextArea(self, inputid.FNAME, name=self.txt_filename.Name)
        
        self.chk_filename = CheckBox(self, chkid.FNAME, GT(u'Use "Name" as output filename (<Name>.desktop)'),
                name=u'filename chk', defaultValue=True)
        
        # --- NAME (menu)
        txt_name = wx.StaticText(self, label=GT(u'Name'), name=u'name*')
        self.labels.append(txt_name)
        self.ti_name = TextArea(self, name=u'Name')
        self.ti_name.req = True
        self.opts_input.append(self.ti_name)
        
        # --- EXECUTABLE
        txt_exec = wx.StaticText(self, label=GT(u'Executable'), name=u'exec')
        self.labels.append(txt_exec)
        
        self.ti_exec = TextArea(self, name=u'Exec')
        self.opts_input.append(self.ti_exec)
        
        # --- COMMENT
        txt_comm = wx.StaticText(self, label=GT(u'Comment'), name=u'comment')
        self.labels.append(txt_comm)
        
        self.ti_comm = TextArea(self, name=u'Comment')
        self.opts_input.append(self.ti_comm)
        
        # --- ICON
        txt_icon = wx.StaticText(self, label=GT(u'Icon'), name=u'icon')
        self.labels.append(txt_icon)
        
        self.ti_icon = TextArea(self, name=u'Icon')
        self.opts_input.append(self.ti_icon)
        
        # --- TYPE
        opts_type = (u'Application', u'Link', u'Directory',)
        
        txt_type = wx.StaticText(self, label=GT(u'Type'), name=u'type')
        self.labels.append(txt_type)
        
        self.ti_type = ComboBox(self, value=opts_type[0], choices=opts_type, name=u'Type')
        self.ti_type.default = self.ti_type.GetValue()
        self.opts_input.append(self.ti_type)
        
        # --- TERMINAL
        opts_term = (u'true', u'false',)
        
        txt_term = wx.StaticText(self, label=GT(u'Terminal'), name=u'terminal')
        self.labels.append(txt_term)
        
        self.sel_term = Choice(self, choices=opts_term, name=u'Terminal',
                defaultValue=1)
        self.opts_choice.append(self.sel_term)
        
        # --- STARTUP NOTIFY
        self.notify_opt = (u'true', u'false',)
        
        txt_notify = wx.StaticText(self, label=GT(u'Startup Notify'), name=u'startupnotify')
        self.labels.append(txt_notify)
        
        self.sel_notify = Choice(self, choices=self.notify_opt, name=u'StartupNotify')
        self.opts_choice.append(self.sel_notify)
        
        # --- ENCODING
        opts_enc = (
            u'UTF-1', u'UTF-7', u'UTF-8', u'CESU-8', u'UTF-EBCDIC',
            u'UTF-16', u'UTF-32', u'SCSU', u'BOCU-1', u'Punycode',
            u'GB 18030',
            )
        
        txt_enc = wx.StaticText(self, label=GT(u'Encoding'), name=u'encoding')
        self.labels.append(txt_enc)
        
        self.ti_enc = ComboBox(self, value=opts_enc[2], choices=opts_enc, name=u'Encoding')
        self.ti_enc.default = self.ti_enc.GetValue()
        self.opts_input.append(self.ti_enc)
        
        # --- CATEGORIES
        opts_category = (
            u'2DGraphics',
            u'Accessibility', u'Application', u'ArcadeGame', u'Archiving', u'Audio', u'AudioVideo',
            u'BlocksGame', u'BoardGame',
            u'Calculator', u'Calendar', u'CardGame', u'Compression', u'ContactManagement', u'Core',
            u'DesktopSettings', u'Development', u'Dictionary', u'DiscBurning', u'Documentation',
            u'Email',
            u'FileManager', u'FileTransfer',
            u'Game', u'GNOME', u'Graphics', u'GTK',
            u'HardwareSettings',
            u'InstantMessaging',
            u'KDE',
            u'LogicGame',
            u'Math', u'Monitor',
            u'Network',
            u'OCR', u'Office',
            u'P2P', u'PackageManager', u'Photography', u'Player', u'Presentation', u'Printing',
            u'Qt',
            u'RasterGraphics', u'Recorder', u'RemoteAccess',
            u'Scanning', u'Screensaver', u'Security', u'Settings', u'Spreadsheet', u'System',
            u'Telephony', u'TerminalEmulator', u'TextEditor',
            u'Utility',
            u'VectorGraphics', u'Video', u'Viewer',
            u'WordProcessor', u'Wine', u'Wine-Programs-Accessories',
            u'X-GNOME-NetworkSettings', u'X-GNOME-PersonalSettings', u'X-GNOME-SystemSettings',
            u'X-KDE-More', u'X-Red-Hat-Base', u'X-SuSE-ControlCenter-System',
            )
        
        txt_category = wx.StaticText(self, label=GT(u'Category'), name=u'category')
        self.labels.append(txt_category)
        
        # This option does not get set by importing a new project
        self.ti_category = ComboBox(self, value=opts_category[0], choices=opts_category,
                name=txt_category.Name)
        self.ti_category.default = self.ti_category.GetValue()
        self.opts_input.append(self.ti_category)
        
        btn_catadd = ButtonAdd(self, name=u'add category')
        btn_catdel = ButtonRemove(self, name=u'rm category')
        btn_catclr = ButtonClear(self, name=u'clear categories')
        
        for B in btn_catadd, btn_catdel, btn_catclr:
            self.opts_button.append(B)
        
        # FIXME: Allow using multi-select + remove
        self.lst_categories = ListCtrl(self)
        # Can't set LC_SINGLE_SEL in constructor for wx 3.0 (ListCtrl bug???)
        self.lst_categories.SetSingleStyle(wx.LC_SINGLE_SEL)
        
        # For manually setting background color after enable/disable
        self.lst_categories.default_color = self.lst_categories.GetBackgroundColour()
        self.lst_categories.SetName(u'Categories')
        self.opts_list.append(self.lst_categories)
        
        # ----- MISC
        txt_other = wx.StaticText(self, label=GT(u'Other'), name=u'other')
        self.labels.append(txt_other)
        
        self.ti_other = TextAreaPanel(self, name=txt_other.Name)
        self.ti_other.default = wx.EmptyString
        self.ti_other.EnableDropTarget()
        self.opts_input.append(self.ti_other)
        
        self.OnToggle()
        
        SetPageToolTips(self)
        
        # *** Layout *** #
        
        CENTER_EXPAND = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND
        CENTER_RIGHT = wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT
        LEFT_CENTER = wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL
        LEFT_BOTTOM = wx.ALIGN_LEFT|wx.ALIGN_BOTTOM
        RIGHT_CENTER = wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL
        
        lyt_buttons = BoxSizer(wx.HORIZONTAL)
        lyt_buttons.Add(btn_open, 0)
        lyt_buttons.Add(btn_save, 0)
        lyt_buttons.Add(btn_preview, 0)
        
        lyt_cat_btn = BoxSizer(wx.HORIZONTAL)
        lyt_cat_btn.Add(btn_catadd, 0)
        lyt_cat_btn.Add(btn_catdel, 0)
        lyt_cat_btn.Add(btn_catclr, 0)
        
        lyt_cat_input = BoxSizer(wx.VERTICAL)
        lyt_cat_input.Add(txt_category, 0, LEFT_BOTTOM)
        lyt_cat_input.Add(self.ti_category, 0, wx.TOP|wx.BOTTOM, 5)
        lyt_cat_input.Add(lyt_cat_btn, 0)
        
        lyt_cat_main = BoxSizer(wx.HORIZONTAL)
        lyt_cat_main.Add(lyt_cat_input, 0)
        lyt_cat_main.Add(self.lst_categories, 1, wx.EXPAND|wx.LEFT, 5)
        
        lyt_grid = wx.GridBagSizer(5, 5)
        lyt_grid.SetCols(4)
        lyt_grid.AddGrowableCol(1)
        
        # Row 1
        lyt_grid.Add(self.txt_filename, (0, 0), flag=RIGHT_CENTER)
        lyt_grid.Add(self.ti_filename, pos=(0, 1), flag=CENTER_EXPAND)
        lyt_grid.Add(self.chk_filename, pos=(0, 2), span=(1, 2), flag=CENTER_RIGHT)
        
        # Row 2
        lyt_grid.Add(txt_name, (1, 0), flag=RIGHT_CENTER)
        lyt_grid.Add(self.ti_name, (1, 1), flag=CENTER_EXPAND)
        lyt_grid.Add(txt_type, (1, 2), flag=RIGHT_CENTER)
        lyt_grid.Add(self.ti_type, (1, 3), flag=CENTER_EXPAND)
        
        # Row 3
        lyt_grid.Add(txt_exec, (2, 0), flag=RIGHT_CENTER)
        lyt_grid.Add(self.ti_exec, (2, 1), flag=CENTER_EXPAND)
        lyt_grid.Add(txt_term, (2, 2), flag=RIGHT_CENTER)
        lyt_grid.Add(self.sel_term, (2, 3), flag=LEFT_CENTER)
        
        # Row 4
        lyt_grid.Add(txt_comm, (3, 0), flag=RIGHT_CENTER)
        lyt_grid.Add(self.ti_comm, (3, 1), flag=CENTER_EXPAND)
        lyt_grid.Add(txt_notify, (3, 2), flag=RIGHT_CENTER)
        lyt_grid.Add(self.sel_notify, (3, 3), flag=LEFT_CENTER)
        
        # Row 5
        lyt_grid.Add(txt_icon, (4, 0), flag=RIGHT_CENTER)
        lyt_grid.Add(self.ti_icon, (4, 1), flag=CENTER_EXPAND)
        lyt_grid.Add(txt_enc, (4, 2), flag=RIGHT_CENTER)
        lyt_grid.Add(self.ti_enc, (4, 3), flag=CENTER_EXPAND)
        
        lyt_border = BoxSizer(wx.VERTICAL)
        
        lyt_border.Add(lyt_grid, 0, wx.EXPAND|wx.BOTTOM, 5)
        lyt_border.Add(lyt_cat_main, 0, wx.EXPAND|wx.TOP, 5)
        lyt_border.AddSpacer(5)
        lyt_border.Add(txt_other, 0)
        lyt_border.Add(self.ti_other, 1, wx.EXPAND)
        
        # --- Page 5 Sizer --- #
        lyt_main = BoxSizer(wx.VERTICAL)
        lyt_main.AddSpacer(5)
        lyt_main.Add(lyt_buttons, 0, wx.ALIGN_RIGHT|wx.RIGHT|wx.BOTTOM, 5)
        lyt_main.Add(self.chk_enable, 0, wx.LEFT, 5)
        lyt_main.Add(lyt_border, 1, wx.EXPAND|wx.ALL, 5)
        
        self.SetAutoLayout(True)
        self.SetSizer(lyt_main)
        self.Layout()
        
        # *** Event handlers *** #
        
        btn_open.Bind(wx.EVT_BUTTON, self.OnLoadLauncher)
        btn_save.Bind(wx.EVT_BUTTON, self.OnSaveLauncher)
        btn_preview.Bind(wx.EVT_BUTTON, self.OnPreviewLauncher)
        
        self.chk_enable.Bind(wx.EVT_CHECKBOX, self.OnToggle)
        
        self.chk_filename.Bind(wx.EVT_CHECKBOX, self.OnSetCustomFilename)
        
        wx.EVT_KEY_DOWN(self.ti_category, self.SetCategory)
        wx.EVT_KEY_DOWN(self.lst_categories, self.SetCategory)
        btn_catadd.Bind(wx.EVT_BUTTON, self.SetCategory)
        btn_catdel.Bind(wx.EVT_BUTTON, self.SetCategory)
        btn_catclr.Bind(wx.EVT_BUTTON, self.SetCategory)
    
    
    ## TODO: Doxygen
    def ExportPage(self):
        return self.GetLauncherInfo()
    
    
    ## TODO: Doxygen
    def GatherData(self):
        if self.chk_enable.GetValue():
            data = self.GetLauncherInfo()
            data = u'\n'.join(data.split(u'\n')[1:])
            
            if not self.chk_filename.GetValue():
                data = u'[FILENAME={}]\n{}'.format(self.ti_filename.GetValue(), data)
            
            return u'<<MENU>>\n1\n{}\n<</MENU>>'.format(data)
        
        else:
            return u'<<MENU>>\n0\n<</MENU>>'
    
    
    ## Formats the launcher information for export
    def GetLauncherInfo(self):
        desktop_list = [u'[Desktop Entry]']
        
        name = self.ti_name.GetValue()
        if not TextIsEmpty(name):
            desktop_list.append(u'Name={}'.format(name))
        
        desktop_list.append(u'Version=1.0')
        
        executable = self.ti_exec.GetValue()
        if not TextIsEmpty(executable):
            desktop_list.append(u'Exec={}'.format(executable))
        
        comment = self.ti_comm.GetValue()
        if not TextIsEmpty(comment):
            desktop_list.append(u'Comment={}'.format(comment))
        
        icon = self.ti_icon.GetValue()
        if not TextIsEmpty(icon):
            desktop_list.append(u'Icon={}'.format(icon))
        
        launcher_type = self.ti_type.GetValue()
        if not TextIsEmpty(launcher_type):
            desktop_list.append(u'Type={}'.format(launcher_type))
        
        desktop_list.append(u'Terminal={}'.format(GS(self.sel_term.GetSelection() == 0).lower()))
        
        desktop_list.append(u'StartupNotify={}'.format(GS(self.sel_notify.GetSelection() == 0).lower()))
        
        encoding = self.ti_enc.GetValue()
        if not TextIsEmpty(encoding):
            desktop_list.append(u'Encoding={}'.format(encoding))
        
        categories = []
        cat_total = self.lst_categories.GetItemCount()
        count = 0
        while count < cat_total:
            C = self.lst_categories.GetItemText(count)
            if not TextIsEmpty(C):
                categories.append(self.lst_categories.GetItemText(count))
            
            count += 1
        
        # Add a final semi-colon if categories is not empty
        if categories:
            categories = u';'.join(categories)
            if categories[-1] != u';':
                categories = u'{};'.format(categories)
            
            desktop_list.append(u'Categories={}'.format(categories))
        
        other = self.ti_other.GetValue()
        if not TextIsEmpty(other):
            desktop_list.append(other)
        
        return u'\n'.join(desktop_list)
    
    
    ## Retrieves the filename to be used for the menu launcher
    def GetOutputFilename(self):
        if not self.chk_filename.GetValue():
            filename = self.ti_filename.GetValue().strip(u' ').replace(u' ', u'_')
            if not TextIsEmpty(filename):
                return filename
        
        return self.ti_name.GetValue().strip(u' ').replace(u' ', u'_')
    
    
    ## TODO: Doxygen
    def IsBuildExportable(self):
        return self.chk_enable.GetValue()
    
    
    ## Loads a .desktop launcher's data
    #  
    #  FIXME: Might be problems with reading/writing launchers (see OnSaveLauncher)
    #         'Others' field not being completely filled out.
    def OnLoadLauncher(self, event=None):
        dia = wx.FileDialog(GetMainWindow(), GT(u'Open Launcher'), os.getcwd(),
                style=wx.FD_CHANGE_DIR)
        
        if ShowDialog(dia):
            path = dia.GetPath()
            
            data = ReadFile(path, split=True)
            
            # Remove unneeded lines
            if data[0] == u'[Desktop Entry]':
                data = data[1:]
            
            self.Reset()
            self.SetLauncherData(u'\n'.join(data))
    
    
    ## TODO: Doxygen
    def OnPreviewLauncher(self, event=None):
        # Show a preview of the .desktop config file
        config = self.GetLauncherInfo()
        
        dia = TextPreview(title=GT(u'Menu Launcher Preview'),
                text=config, size=(500,400))
        
        dia.ShowModal()
        dia.Destroy()
    
    
    ## Saves launcher information to file
    #  
    #  FIXME: Might be problems with reading/writing launchers (see OnLoadLauncher)
    #         'Others' field not being completely filled out.
    def OnSaveLauncher(self, event=None):
        Logger.Debug(__name__, u'Export launcher ...')
        
        # Get data to write to control file
        menu_data = self.GetLauncherInfo().encode(u'utf-8')
        
        dia = wx.FileDialog(GetMainWindow(), GT(u'Save Launcher'), os.getcwd(),
            style=wx.FD_SAVE|wx.FD_CHANGE_DIR|wx.FD_OVERWRITE_PROMPT)
        
        if ShowDialog(dia):
            path = dia.GetPath()
            
            # Create a backup file
            overwrite = False
            if os.path.isfile(path):
                backup = u'{}.backup'.format(path)
                shutil.copy(path, backup)
                overwrite = True
            
            try:
                WriteFile(path, menu_data)
                
                if overwrite:
                    os.remove(backup)
            
            except UnicodeEncodeError:
                detail1 = GT(u'Unfortunately Debreate does not support unicode yet.')
                detail2 = GT(u'Remove any non-ASCII characters from your project.')
                
                ShowErrorDialog(GT(u'Save failed'), u'{}\n{}'.format(detail1, detail2), title=GT(u'Unicode Error'))
                
                os.remove(path)
                # Restore from backup
                shutil.move(backup, path)
    
    
    ## TODO: Doxygen
    def OnSetCustomFilename(self, event=None):
        if not self.chk_filename.IsEnabled():
            self.txt_filename.Enable(False)
            self.ti_filename.Enable(False)
            return
        
        if self.chk_filename.GetValue():
            self.txt_filename.Enable(False)
            self.ti_filename.Enable(False)
            return
        
        self.txt_filename.Enable(True)
        self.ti_filename.Enable(True)
    
    
    ## TODO: Doxygen
    def OnToggle(self, event=None):
        enable = self.chk_enable.IsChecked()
        
        listctrl_bgcolor_defs = {
            True: self.lst_categories.default_color,
            False: wx.Colour(214, 214, 214),
        }
        
        for group in self.opts_button, self.opts_choice, self.opts_input, \
                self.opts_list, self.labels:
            for O in group:
                O.Enable(enable)
                
                # Small hack to gray-out ListCtrl when disabled
                if isinstance(O, wx.ListCtrl):
                    O.SetBackgroundColour(listctrl_bgcolor_defs[enable])
        
        self.chk_filename.Enable(enable)
        self.OnSetCustomFilename()
    
    
    ## TODO: Doxygen
    def Reset(self):
        self.chk_filename.SetValue(self.chk_filename.default)
        self.ti_filename.Clear()
        
        for O in self.opts_input:
            O.SetValue(O.default)
        
        for O in self.opts_choice:
            O.SetSelection(O.default)
        
        for O in self.opts_list:
            O.DeleteAllItems()
        
        self.chk_enable.SetValue(self.chk_enable.default)
        self.OnToggle()
    
    
    ## TODO: Doxygen
    def SetCategory(self, event=None):
        try:
            ID = event.GetKeyCode()
        
        except AttributeError:
            ID = event.GetEventObject().GetId()
        
        cat = self.ti_category.GetValue()
        cat = cat.split()
        cat = u''.join(cat)
        
        if ID in (wx.ID_ADD, wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER):
            self.lst_categories.InsertStringItem(self.lst_categories.GetItemCount(), cat)
        
        elif ID in (wx.ID_REMOVE, wx.WXK_DELETE):
            if self.lst_categories.GetItemCount() and self.lst_categories.GetSelectedItemCount():
                cur_cat = self.lst_categories.GetFirstSelected()
                self.lst_categories.DeleteItem(cur_cat)
        
        elif ID == wx.ID_CLEAR:
            if self.lst_categories.GetItemCount():
                if ConfirmationDialog(GetMainWindow(), GT(u'Confirm'),
                        GT(u'Clear categories?')).ShowModal() in (wx.ID_OK, wx.OK):
                    self.lst_categories.DeleteAllItems()
        
        if event:
            event.Skip()
    
    
    ## Fills out launcher information from loaded file
    #  
    #  \param data
    #    Information to fill out menu launcher fields
    #  \param enabled
    #    \b \e bool : Launcher will be flagged for export if True
    def SetLauncherData(self, data, enabled=True):
        # Make sure we are dealing with a list
        if isinstance(data, (unicode, str)):
            data = data.split(u'\n')
        
        # Data list is not empty
        if data:
            Logger.Debug(__name__, u'Loading launcher')
            
            if data[0].isnumeric():
                enabled = int(data.pop(0)) > 0
            
            if DebugEnabled():
                for L in data:
                    print(u'  Launcher line: {}'.format(L))
            
            Logger.Debug(__name__, u'Enabling launcher: {}'.format(enabled))
            
            if enabled:
                self.chk_enable.SetValue(True)
                
                data_defs = {}
                data_defs_remove = []
                misc_defs = []
                
                for L in data:
                    if u'=' in L:
                        if L[0] == u'[' and L[-1] == u']':
                            key = L[1:-1].split(u'=')
                            value = key[1]
                            key = key[0]
                            
                            misc_defs.append(u'{}={}'.format(key, value))
                        
                        else:
                            key = L.split(u'=')
                            value = key[1]
                            key = key[0]
                            
                            data_defs[key] = value
                
                # Fields using SetValue() function
                set_value_fields = (
                    (u'Name', self.ti_name),
                    (u'Exec', self.ti_exec),
                    (u'Comment', self.ti_comm),
                    (u'Icon', self.ti_icon),
                    (u'Type', self.ti_type),
                    (u'Encoding', self.ti_enc),
                    )
                
                for label, control in set_value_fields:
                    try:
                        control.SetValue(data_defs[label])
                        data_defs_remove.append(label)
                    
                    except KeyError:
                        pass
                
                # Fields using SetSelection() function
                set_selection_fields = (
                    (u'Terminal', self.sel_term),
                    (u'StartupNotify', self.sel_notify),
                    )
                
                for label, control in set_selection_fields:
                    try:
                        control.SetStringSelection(data_defs[label].lower())
                        data_defs_remove.append(label)
                    
                    except KeyError:
                        pass
                
                try:
                    categories = tuple(data_defs[u'Categories'].split(u';'))
                    for C in categories:
                        self.lst_categories.InsertStringItem(self.lst_categories.GetItemCount(), C)
                    
                    data_defs_remove.append(u'Categories')
                
                except KeyError:
                    pass
                
                for K in data_defs_remove:
                    if K in data_defs:
                        del data_defs[K]
                
                # Add any leftover keys to misc/other
                for K in data_defs:
                    if K not in (u'Version',):
                        misc_defs.append(u'{}={}'.format(K, data_defs[K]))
                
                for index in reversed(range(len(misc_defs))):
                    K = misc_defs[index]
                    
                    # Set custom filename
                    if u'FILENAME=' in K:
                        filename = K.replace(u'FILENAME=', u'')
                        
                        if not TextIsEmpty(filename):
                            Logger.Debug(__name__, u'Setting custom filename: {}'.format(filename))
                            
                            self.ti_filename.SetValue(filename)
                            self.chk_filename.SetValue(False)
                        
                        # Remove so not added to misc. list
                        misc_defs.pop(index)
                        
                        continue
                
                if misc_defs:
                    self.ti_other.SetValue(u'\n'.join(sorted(misc_defs)))
                
                self.OnToggle()
