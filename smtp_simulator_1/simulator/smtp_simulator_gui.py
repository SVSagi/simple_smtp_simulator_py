import ss_tray
import wx.html
import smtp_simulator_server as smtp_ss
import os, email, datetime, time, threading

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
        self.eml_table.InsertColumn(5, 'Email', width=50)
        
        self.et_bs1 = wx.BoxSizer(wx.VERTICAL)
        self.et_bs1.Add(self.eml_table, 1, wx.EXPAND|wx.ALL)
        self.SetSizerAndFit(self.et_bs1)
        
        '''
        self.il = wx.ImageList(16, 16)
        img_idx = self.il.Add(wx.Image("icons/attach.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        self.eml_table.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
        
        self.eml_table.InsertStringItem(0, "23:42 26-11-2014")
        self.eml_table.SetStringItem(0, 1, "maxadmin@maximo.com")
        self.eml_table.SetStringItem(0, 2, "user1@maximo.com")
        self.eml_table.SetStringItem(0, 3, "Your Maximo passwors was changed")
        self.eml_table.SetStringItem(0, 4, "PDF")

        #self.eml_table.SetItemImage(0, 1, img_idx)
        #self.eml_table.InsertImageStringItem(1, "", img_idx)
        #self.eml_table.Append(("15:20 28-11-2014", "user3@client.com"))
        '''
        
        self.eml_table.Bind(wx.EVT_LEFT_DOWN, self.OnListLeftDown)
        self.eml_table.Bind(wx.EVT_RIGHT_DOWN, self.OnListRightDown)
        
        self.loadEmailFiles(None)
     
    def deleteEmailFile(self, event):
        index = self.eml_table.GetFirstSelected()
        item = self.eml_table.GetItem(itemId=index, col=5)
        os.remove('emails/'+item.GetText())
        self.eml_table.DeleteItem(index)
        
    def OnListLeftDown(self, event):
        x,y = event.GetPosition()
        row,flags = self.eml_table.HitTest( (x,y) )
        #self.Parent.Parent.ED_panel.html_win.SetPage('<html><body><i>Email: '+str(row)+'</i></body></html>')
        #count = self.eml_table.GetItemCount()
        #cols = self.eml_table.GetColumnCount()
        
        item = self.eml_table.GetItem(itemId=row, col=5)
        #print item.GetText()
        f1 = open('emails/'+item.GetText()) 
        emsg = email.message_from_string(str(f1.read()))
        f1.close()
        self.Parent.Parent.ED_panel.html_win.SetPage('<html>'+self.getEmailBody(emsg)+'</html>')
        self.eml_table.Select(row)
            
    def OnListRightDown(self, event):
        pass
    
    def loadEmailFiles(self, event):
        self.eml_table.DeleteAllItems()
        for file in os.listdir("emails"):
            if file.endswith(".eml"):
                f1 = open('emails/'+file) 
                emsg = email.message_from_string(str(f1.read()))
                f1.close()
                self.eml_table.Append((emsg['date'], emsg['from'], emsg['to'], emsg['subject'], '', file))#os.path.splitext(file)[0]
        print 'Emails Loaded'
                
    def getEmailBody(self, emsg):
        body = ""
        if emsg.is_multipart():
            for payload in emsg.get_payload():
                body+= payload.get_payload()
        else:
            body =  emsg.get_payload()
                
        return body        

class EmailDetailsPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.ed_bs1= wx.BoxSizer()
        self.html_win = wx.html.HtmlWindow(self)
        self.ed_bs1.Add(self.html_win, proportion=1, flag=wx.CENTER|wx.EXPAND)
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
        wx.Frame.__init__(self, None, title=app_name+" v"+app_version, size=(700, 500), pos=(100, 100))
        self.main_panel = MainPanel(self)
        self.status_bar = self.CreateStatusBar()
        self.status_bar.SetFieldsCount(2)
        self.status_bar.SetStatusWidths([80,-1])
        self.tbIcon = ss_tray.TrayIcon(self)
        self.last_eml = ""
        
        self.smtp_mgnr = None
        self.mon_thread = None
        self.stop_mon = False
 
        self.Bind(wx.EVT_ICONIZE, self.onMinimize)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        
        toolbar = self.CreateToolBar(wx.TB_NODIVIDER | wx.TB_FLAT | wx.TB_DOCKABLE)
        startTool = toolbar.AddLabelTool(wx.ID_ANY, 'Start', wx.Bitmap('icons/computer.png'), shortHelp='Start Simulator')
        stopTool  = toolbar.AddLabelTool(wx.ID_ANY, 'Stop', wx.Bitmap('icons/computer_delete.png'), shortHelp='Stop Simulator')
        refresh_emls  = toolbar.AddLabelTool(wx.ID_ANY, 'Refresh', wx.Bitmap('icons/arrow_refresh.png'), shortHelp='Refresh Emails')
        monitor_emails  = toolbar.AddLabelTool(wx.ID_ANY, 'Monitor', wx.Bitmap('icons/flag_blue.png'), shortHelp='Monitor Emails')
        stop_monitor_emails  = toolbar.AddLabelTool(wx.ID_ANY, 'Stop Monitor', wx.Bitmap('icons/flag_red.png'), shortHelp='Stop Monitoring Emails')
        delete_sel_eml  = toolbar.AddLabelTool(wx.ID_ANY, 'Delete Email', wx.Bitmap('icons/delete.png'), shortHelp='Delete Selected Email')
        toolbar.Realize()

        self.Bind(wx.EVT_TOOL, self.startSMTPSS, startTool)
        self.Bind(wx.EVT_TOOL, self.stopSMTPSS, stopTool)
        self.Bind(wx.EVT_TOOL, self.main_panel.ET_panel.loadEmailFiles, refresh_emls)
        self.Bind(wx.EVT_TOOL, self.doMonitor, monitor_emails)
        self.Bind(wx.EVT_TOOL, self.stopMonitor, stop_monitor_emails)
        self.Bind(wx.EVT_TOOL, self.main_panel.ET_panel.deleteEmailFile, delete_sel_eml)
        
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
        
        self.Bind(wx.EVT_MENU, self.onClose, id=13)
        
        self.SetIcon(wx.Icon('icons/shape_square.png', wx.BITMAP_TYPE_PNG))
        
        self.Show()
        
    def doMonitor(self, event):
        print '#Start Monitor'
        
        if self.smtp_mgnr==None or not self.smtp_mgnr.thread.isAlive():
            print 'Server Not started to Monitor' 
            return
            
        if self.mon_thread!=None and self.mon_thread.isAlive():
            print 'Already Monitoring'
            return
                
        self.mon_thread =  threading.Thread(target=self.checkForNewEmails )
        self.mon_thread.start()
    
    def stopMonitor(self, event):
        print '#Stop Monitor'
        if self.mon_thread==None or not self.mon_thread.isAlive():
            print 'Not monitoring'
            return
        
        self.stop_mon = True    
        
    def checkForNewEmails(self):
        
        while not self.stop_mon:

            if smtp_ss.last_eml=="":
                continue
            
            if self.last_eml != smtp_ss.last_eml:
                print 'You Have New Email'+  smtp_ss.last_eml
                self.main_panel.ET_panel.loadEmailFiles(None)
                self.last_eml = smtp_ss.last_eml

            #time.sleep(1)
        
        print 'Stopped Monitoring for Mails'
 
    def startSMTPSS(self, event):
        if self.smtp_mgnr!=None and self.smtp_mgnr.thread.isAlive():
            print 'Already Running'
            return
        
        self.smtp_mgnr = smtp_ss.ServerManager()
        self.smtp_mgnr.start()

    def stopSMTPSS(self, event):
        if self.smtp_mgnr==None:
            print 'Not Started'
            return
        
        if not self.smtp_mgnr.thread.isAlive():    
            print 'Not Running'
            return
            
        self.stopMonitor(event)    
        self.smtp_mgnr.stop()
                
    def onClose(self, event):
        self.stopSMTPSS(event)
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
    
'''    
server = test.MyReceiver()
server.start()
app = wx.App(False)
frame = MainFrame()
app.MainLoop()
time.sleep(10)
server.stop()
'''    