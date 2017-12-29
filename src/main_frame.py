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

        self.playgame = lianliankan.PlayGame()
        self.retrycnt = 0

    def regHotKey(self):
        self.hotKeyId = 100
        self.RegisterHotKey(
            self.hotKeyId,
            0,
            win32con.VK_F1)

    def regHotKey2(self):
        self.hotKeyId2 = 101
        self.RegisterHotKey(
            self.hotKeyId2,
            0,
            win32con.VK_F2)

    def regHotKey3(self):
        self.hotKeyId3 = 102
        self.RegisterHotKey(
            self.hotKeyId3,
            0,
            win32con.VK_F3)

    def handleHotKey(self, evt):
        self.t = self.playgame.solve_all()
        self.timer.Start(100)

    def handleHotKey2(self, evt):
        if self.timer.IsRunning():
            print('pause')
            self.timer.Stop()
        else:
            print('resume')
            self.timer.Start(100)

    def handleHotKey3(self, evt):
        print('change super mode')
        self.playgame.switch_super()

    def on_timer(self, event):
        try:
            self.t.__next__()
        except:
            self.retrycnt += 1
            if self.retrycnt < 2:
                self.t = self.playgame.solve_all()
            else:
                self.retrycnt = 0
                self.timer.Stop()

    def on_click(self, event):
        self.t = self.playgame.solve_all()
        self.t.__next__()
        self.timer.Start(100)


app = wx.App()

frm = FrameWithHotKey(None, title='Super LianLianKan')
frm.Show()
app.MainLoop()