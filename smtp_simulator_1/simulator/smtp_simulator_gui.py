import ss_tray
import wx

app_name = "SMTP Simulator"
app_version = "0.1b1"

class EmailTablePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        self.eml_table = wx.ListCtrl(self, style=wx.LC_REPORT|wx.BORDER_NONE|wx.LC_SINGLE_SEL)
        self.eml_table.InsertColumn(0, 'Date', width=100)
        self.eml_table.InsertColumn(1, 'From', width=120)
        self.eml_table.InsertColumn(2, 'To', width=120)
        self.eml_table.InsertColumn(3, 'Subject', width=180)
        self.eml_table.InsertColumn(4, 'Attachment', width=50)
        self.eml_table.InsertColumn(5, 'Email ID', width=50)
        
        self.et_bs1 = wx.BoxSizer(wx.VERTICAL)
        self.et_bs1.Add(self.eml_table, 1, wx.EXPAND|wx.ALL)
        self.SetSizerAndFit(self.et_bs1)
        
        '''
        self.il = wx.ImageList(16, 16)
        img_idx = self.il.Add(wx.Image("icons/attach.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        self.eml_table.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
        '''
        self.eml_table.InsertStringItem(0, "23:42 26-11-2014")
        self.eml_table.SetStringItem(0, 1, "maxadmin@maximo.com")
        self.eml_table.SetStringItem(0, 2, "user1@maximo.com")
        self.eml_table.SetStringItem(0, 3, "Your Maximo passwors was changed")
        self.eml_table.SetStringItem(0, 4, "PDF")
        
        self.eml_table.InsertStringItem(1, "23:20 26-11-2014")
        self.eml_table.SetStringItem(1, 1, "maxadmin@maximo.com")
        self.eml_table.SetStringItem(1, 2, "2@maximo.com")
        self.eml_table.SetStringItem(1, 3, "Your Maximo passwors was changed")
        self.eml_table.SetStringItem(1, 4, "PDF")
        #self.eml_table.SetItemImage(0, 1, img_idx)
        #self.eml_table.InsertImageStringItem(1, "", img_idx) 
        
        self.eml_table.Bind(wx.EVT_LEFT_DOWN, self.OnListLeftDown)
        self.eml_table.Bind(wx.EVT_RIGHT_DOWN, self.OnListRightDown)
        
    def OnListLeftDown(self, event):
        x,y = event.GetPosition()
        row,flags = self.eml_table.HitTest( (x,y) )
        print row
        self.eml_table.Select(row)
            
    def OnListRightDown(self, event):
        pass

class EmailDetailsPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.ed_bs1= wx.BoxSizer()
        self.xmlE = wx.TextCtrl(self, id=wx.ID_ANY, style=wx.TE_MULTILINE|wx.BORDER_NONE|wx.EXPAND|wx.TE_DONTWRAP|wx.TE_RICH2)
        self.ed_bs1.Add(self.xmlE, proportion=1, flag=wx.CENTER|wx.EXPAND)
        self.SetSizerAndFit(self.ed_bs1)

class MainPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
 
        self.sptr1 = wx.SplitterWindow(self)
 
        self.ET_panel = EmailTablePanel(self.sptr1)
        self.ED_panel = EmailDetailsPanel(self.sptr1)
 
        self.sptr1.SplitHorizontally(self.ET_panel, self.ED_panel)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.sptr1, 1, wx.EXPAND)
        self.SetSizer(sizer)
        
        self.sptr1.SetSashPosition(200)
        #self.sptr1.Bind(wx.EVT_SPLITTER_DCLICK, self.splitResize)
        

class MainFrame(wx.Frame):
    
    def __init__(self):
        wx.Frame.__init__(self, None, title=app_name+" v"+app_version, size=(600, 500), pos=(400, 100))
        self.main_panel = MainPanel(self)
        self.status_bar = self.CreateStatusBar()
        self.status_bar.SetFieldsCount(2)
        self.status_bar.SetStatusWidths([80,-1])
        self.tbIcon = ss_tray.TrayIcon(self)
 
        self.Bind(wx.EVT_ICONIZE, self.onMinimize)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        
        toolbar = self.CreateToolBar(wx.TB_NODIVIDER | wx.TB_FLAT | wx.TB_DOCKABLE)
        startTool = toolbar.AddLabelTool(wx.ID_ANY, 'Start', wx.Bitmap('icons/computer.png'), shortHelp='Start Simulator')
        stopTool  = toolbar.AddLabelTool(wx.ID_ANY, 'Stop', wx.Bitmap('icons/computer_delete.png'), shortHelp='Stop Simulator')
        toolbar.Realize()

        self.Bind(wx.EVT_TOOL, self.onClose, startTool)
        self.Bind(wx.EVT_TOOL, self.onClose, stopTool)
        
        menuBar = wx.MenuBar()

        serverMenu = wx.Menu()
        aboutMenu = wx.Menu()
        
        serverMenu.AppendItem(wx.MenuItem(serverMenu, 11, 'Start&\tAlt+Q'))
        serverMenu.AppendItem(wx.MenuItem(serverMenu, 12, 'Stop&\tAlt+W'))
        serverMenu.AppendItem(wx.MenuItem(serverMenu, 13, 'Exit&\tAlt+E'))
        
        aboutMenu.AppendItem(wx.MenuItem(aboutMenu, 21, 'About'))
        
        menuBar.Append(serverMenu, "&Simulator")
        menuBar.Append(aboutMenu,  "&Help")
        self.SetMenuBar(menuBar)
        
        self.SetIcon(wx.Icon('icons/shape_square.png', wx.BITMAP_TYPE_PNG))
        
        self.Show()
 
    def onClose(self, evt):
        self.tbIcon.RemoveIcon()
        self.tbIcon.Destroy()
        self.Destroy()
 
    def onMinimize(self, event):
        self.Hide()
 
def main():
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()
 
if __name__ == "__main__":
    main()