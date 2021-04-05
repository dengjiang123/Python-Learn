import wx

app=wx.App()
image=wx.Image("wxPython.jpg",wx.BITMAP_TYPE_JPEG)
temp=image.ConvertToBitmap()
size=temp.GetWidth(),temp.GetHeight()
print(size)
frame=wx.Frame(None,title="test1",size=size)
wx.StaticBitmap(parent=frame,bitmap=temp)
frame.SetClientSize(size)
frame.Show()
app.MainLoop()
