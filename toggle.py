# coding=utf-8
import wx
import warnings
import time

warnings.filterwarnings(action='ignore')
class ButtonFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'Button Example',
                          size=(300, 100))
        panel = wx.Panel(self, -1)
        self.button = wx.Button(panel, -1, "Hello", pos=(50, 20))
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.button)
        self.button.SetDefault()

    def OnClick(self, event):
        if self.button.GetLabel() == "ON":
            self.button.SetLabel("OFF")
        else:
            self.button.SetLabel("ON")

    def autoClick(self, value):
        self.button.SetLabel(value)


if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = ButtonFrame()
    # next_frame = ButtonFrame()
    frame.Show()

    for i in range(10):
        time.sleep(0.1)
        frame.autoClick('111')
        time.sleep(0.1)
        frame.autoClick('222')


    # next_frame.Show()
    app.MainLoop()