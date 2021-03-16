
import wx

def add(event):
    s1=int(num1.GetValue())
    s2=int(num2.GetValue())
    ans.SetValue(str(s1+s2))
def sub(event):
    s1=int(num1.GetValue())
    s2=int(num2.GetValue())
    ans.SetValue(str(s1-s2))
def mul(event):
    s1=int(num1.GetValue())
    s2=int(num2.GetValue())
    ans.SetValue(str(s1*s2))
def div(event):
    s1=int(num1.GetValue())
    s2=int(num2.GetValue())
    ans.SetValue(str(s1/s2))

app=wx.App()
win=wx.Frame(None,title="编辑器",size=(500,300))
bkg=wx.Panel(win)

num1=wx.TextCtrl(bkg)
num2=wx.TextCtrl(bkg)
ans=wx.TextCtrl(bkg)
buttonadd=wx.Button(bkg,label="Add")
buttonadd.Bind(wx.EVT_BUTTON,add)
buttonsub=wx.Button(bkg,label="Sub")
buttonsub.Bind(wx.EVT_BUTTON,sub)
buttonmul=wx.Button(bkg,label="Mul")
buttonmul.Bind(wx.EVT_BUTTON,mul)
buttondiv=wx.Button(bkg,label="Div")
buttondiv.Bind(wx.EVT_BUTTON,div)

hbox=wx.BoxSizer()
hbox.Add(num1,proportion=1,flag=wx.LEFT,border=5)
hbox.Add(num2,proportion=1,flag=wx.LEFT,border=5)
hbox.Add(ans,proportion=1,flag=wx.LEFT,border=5)

hbox1=wx.BoxSizer()
hbox1.Add(buttonadd,proportion=1,flag=wx.LEFT,border=20)
hbox1.Add(buttonsub,proportion=1,flag=wx.LEFT,border=20)
hbox1.Add(buttonmul,proportion=1,flag=wx.LEFT,border=20)
hbox1.Add(buttondiv,proportion=1,flag=wx.LEFT,border=20)

vbox=wx.BoxSizer(wx.VERTICAL)
vbox.Add(hbox,proportion=0,flag=wx.EXPAND | wx.ALL,border=5)
vbox.Add(hbox1,proportion=0,flag=wx.EXPAND | wx.ALL,border=5)

bkg.SetSizer(vbox)
win.Show()

app.MainLoop()
