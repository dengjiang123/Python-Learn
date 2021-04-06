import wx

class Frame(wx.Frame):
    def __init__(self,parent,id):
        wx.Frame.__init__(self,parent,id,"test111",size=(300,300))
        self.panel=wx.Panel(self)
        self.button=wx.Button(self.panel,label="1111",pos=(100,50))
        self.button.Bind(wx.EVT_ENTER_WINDOW,self.Enter)
        self.button.Bind(wx.EVT_LEAVE_WINDOW,self.Leave)

    def Enter(self,event):
        self.button.SetLabel("2222")
        event.Skip()
    def Leave(self,event):
        self.button.SetLabel("1111")
        event.Skip()

if __name__=="__main__":
    app=wx.App()
    frame=Frame(parent=None,id=-1)
    frame.Show()
    app.MainLoop()
