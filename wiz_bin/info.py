# -*- coding: utf-8 -*-

## \package wiz_bin.info


import wx

from dbr.custom     import Hyperlink
from dbr.language   import GT
from globals.ident  import ID_GREETING


## TODO: Doxygen
class Panel(wx.ScrolledWindow):
    def __init__(self, parent, name=GT(u'Information')):
        wx.ScrolledWindow.__init__(self, parent, ID_GREETING, name=GT(u'Information'))
        
        self.SetScrollbars(0, 20, 0, 0)
        
        # --- Mode Information
        m1 = GT(u'Welcome to Debreate!')
        m2 = GT(u'Debreate aids in building packages for installation on Debian based systems. Use the arrows located in the top-right corner or the "Page" menu to navigate through the program. For some information on Debian packages use the reference links in the "Help" menu.')
        m3 = GT(u'For a video tutorial check the link below.')
        str_info = u'{}\n\n{}\n\n{}'.format(m1, m2, m3)
        
        # --- Information to be displayed about each mode
        txt_info = wx.StaticText(self, label=str_info)
        # Keep characters within the width of the window
        txt_info.Wrap(600)
        
        lnk_video = Hyperlink(self, wx.ID_ANY, GT(u'Building a Debian Package with Debreate'),
                u'http://www.youtube.com/watch?v=kx4D5eL6HKE')
        
        layout_info = wx.GridSizer()
        
        layout_info.Add(txt_info, 1, wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL)
        
        # *** Layout *** #
        
        layout_main = wx.BoxSizer(wx.VERTICAL)
        layout_main.Add(layout_info, 4, wx.EXPAND|wx.ALIGN_CENTER|wx.ALL, 10)
        layout_main.Add(lnk_video, 2, wx.EXPAND|wx.ALIGN_CENTER)
        
        self.SetAutoLayout(True)
        self.SetSizer(layout_main)
        self.Layout()
