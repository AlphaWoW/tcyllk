import wx
import win32con
import lianliankan

class FrameWithHotKey(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)
        self.regHotKey()
        self.Bind(wx.EVT_HOTKEY, self.handleHotKey, id=self.hotKeyId)
        self.regHotKey2()
        self.Bind(wx.EVT_HOTKEY, self.handleHotKey2, id=self.hotKeyId2)
        self.regHotKey3()
        self.Bind(wx.EVT_HOTKEY, self.handleHotKey3, id=self.hotKeyId3)

        self.btn = wx.Button(self)
        self.Bind(wx.EVT_BUTTON, self.on_click, self.btn)


        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_timer, self.timer)

        self.ToggleWindowStyle(wx.STAY_ON_TOP)

    def regHotKey(self):
        self.hotKeyId = 100
        self.RegisterHotKey(
            self.hotKeyId,
            win32con.MOD_ALT,
            win32con.VK_F1)

    def regHotKey2(self):
        self.hotKeyId2 = 101
        self.RegisterHotKey(
            self.hotKeyId2,
            win32con.MOD_ALT,
            win32con.VK_F2)

    def regHotKey3(self):
        self.hotKeyId3 = 102
        self.RegisterHotKey(
            self.hotKeyId3,
            win32con.MOD_ALT,
            win32con.VK_F3)

    def handleHotKey(self, evt):
        self.timer.Start(100)

    def handleHotKey2(self, evt):
        self.timer.Stop()

    def handleHotKey3(self, evt):
        lianliankan.fuck = not lianliankan.fuck

    def on_timer(self, event):
        self.t.__next__()

    def on_click(self, event):
        self.t = lianliankan.solve_all()
        self.t.__next__()
        self.timer.Start(100)


app = wx.App()

frm = FrameWithHotKey(None, title='hello world')
frm.Show()
app.MainLoop()