# coding=utf-8
"""
模块标题：界面相关
模块功能：显示批量录入框窗口。
开发人员：seakingx
建立时间：2018.04.28
最后修改：2018.04.29
"""
import tkinter as Tk
import wx


class GUIFrame(wx.Frame):
    def __init__(self, app_title, app_size, input_num):
        self.max_len = input_num
        wx.Frame.__init__(self, None, -1, app_title, size=(app_size[0], app_size[1]))
        panel = wx.Panel(self, -1)
        # 按钮显示文字
        self.loadButton = wx.Button(panel, label=u"处理数据")
        # 显示批量输入框

        self.hbox = wx.BoxSizer()
        self.hbox.Add(self.loadButton, proportion=0, flag=wx.LEFT, border=5)
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox.Add(self.hbox, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        self.max_line = self.max_len
        self.max_row = self.max_len
        self.input_matrix = []

        self.init_inputbox(panel)
        panel.SetSizer(self.vbox)

        self.loadButton.Bind(wx.EVT_BUTTON, self.OnLoad, self.loadButton)

    def init_inputbox(self, panel):
        input_box_i = wx.BoxSizer()
        input_label = wx.StaticText(panel, label=" ", size=(20, 20), style=wx.ALIGN_LEFT)
        input_box_i.Add(input_label, proportion=0, flag=wx.LEFT, border=3)
        for i in range(self.max_line):
            input_item = wx.StaticText(panel, label=str(i + 1), size=(50, 20), style=wx.ALIGN_CENTER)
            input_box_i.Add(input_item, proportion=0, flag=wx.LEFT, border=3)

        self.vbox.Add(input_box_i, proportion=0, flag=wx.EXPAND | wx.ALL, border=1)
        for j in range(self.max_row):
            input_box_i = wx.BoxSizer()
            input_list = []
            input_label = wx.StaticText(panel, label=str(j + 1), size=(20, 25), style=wx.ALIGN_LEFT)
            input_box_i.Add(input_label, proportion=0, flag=wx.LEFT, border=3)
            for i in range(self.max_line):
                input_item = wx.TextCtrl(panel, size=(50, 25))
                input_box_i.Add(input_item, proportion=0, flag=wx.LEFT, border=3)
                input_list.append(input_item)

            self.vbox.Add(input_box_i, proportion=0, flag=wx.EXPAND | wx.ALL, border=1)
            self.input_matrix.append(input_list)

    def OnLoad(self, event):
        self.showMsg(u"开始处理", u"提示")

    def showMsg(self, msg, title):
        wx.MessageBox(msg, title, wx.OK | wx.ICON_INFORMATION)


if __name__ == '__main__':
    # 界面提示文字
    show_info = u"数据处理工具"
    app = wx.App()
    # 建立一个10*10的录入窗口
    frame = GUIFrame(show_info, [800, 450], 10)
    frame.Show()
    app.MainLoop()
