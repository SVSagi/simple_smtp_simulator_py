'''
Created on Nov 26, 2014

@author: Sarraju
'''

import wx

def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.AppendItem(item)
    return item
 
class TrayIcon(wx.TaskBarIcon):

    def __init__(self, frame):
        wx.TaskBarIcon.__init__(self)
        self.frame = frame
 
        img = wx.Image("icons/computer.png", wx.BITMAP_TYPE_ANY)
        bmp = wx.BitmapFromImage(img)
        self.icon = wx.EmptyIcon()
        self.icon.CopyFromBitmap(bmp)
 
        self.SetIcon(self.icon, "Restore")
        self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.OnTaskBarLeftClick)
 
    def OnTaskBarActivate(self, evt):
        pass
 
    def OnTaskBarClose(self, evt):
        #self.frame.Close()
        wx.CallAfter(self.frame.Close)
 
    def OnTaskBarLeftClick(self, evt):
        self.frame.Show()
        self.frame.Restore()
        
    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, 'Show Simulator', self.on_hello)
        menu.AppendSeparator()
        create_menu_item(menu, 'Exit', self.on_exit)
        return menu
    
    def on_hello(self, event):
        print 'TODO'

    def on_exit(self, event):
        #self.frame.Close()
        wx.CallAfter(self.frame.Close)
        
        