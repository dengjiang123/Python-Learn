import wx

app=wx.App()
frame=wx.Frame(None,title="test1",size=(400,400))
panel=wx.Panel(frame)
panel.SetBackgroundColour((100,100,100))
panel.Refresh()
frame.Show()
app.MainLoop()
