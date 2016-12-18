#!/usr/bin/python
#coding: utf-8

"""
注册界面
"""

import pymysql
import wx
from signin_user_mysql import Register_UserMysql

class Register_Now_Frame(wx.Frame):
    def __init__(self, main_Frame):
        super(Register_Now_Frame, self).__init__(None, -1, u"普通用户注册界面", size=(300, 200), pos=(100, 100),
                                      style=wx.DEFAULT_FRAME_STYLE ^ (
                                          wx.RESIZE_BORDER | wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX))
        self.main_Frame = main_Frame

        self.panel = wx.Panel(self, -1)
        topLbl = wx.StaticText(self.panel, -1, u"用户注册界面")
        topLbl.SetFont(wx.Font(13, wx.SWISS, wx.NORMAL, wx.BOLD))
        user = wx.StaticText(self.panel, -1, u"用户名:")
        self.user_ctrl = wx.TextCtrl(self.panel, -1, u"输入用户名")
        password = wx.StaticText(self.panel, -1, u"密  码:")
        self.password_ctrl = wx.TextCtrl(self.panel, -1, "", style = wx.TE_PASSWORD)

        btn1 = wx.Button(self.panel, -1, u"立即注册")
        self.Bind(wx.EVT_BUTTON, self.OnButton_1, btn1)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(topLbl, 0, wx.ALL, 5)
        mainSizer.Add(wx.StaticLine(self.panel), 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 5)

        addSizer = wx.FlexGridSizer(cols = 2, hgap = 5, vgap = 5)
        addSizer.AddGrowableCol(1)
        addSizer.Add(user, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        addSizer.Add(self.user_ctrl, 0, wx.EXPAND)
        addSizer.Add(password, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        addSizer.Add(self.password_ctrl, 0, wx.EXPAND)
        addSizer.Add((10, 10))
        addSizer.Add(btn1, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)

        mainSizer.Add(addSizer, 0, wx.EXPAND|wx.ALL, 10)
        self.panel.SetSizer(mainSizer)

        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def OnButton_1(self, event):
        username =self.user_ctrl.GetValue()
        password = self.password_ctrl.GetValue()
        win = Register_UserMysql(username, password)

        # 验证Register_UserMysql当前密码是否存在的表示值
        self.flag = win.GetFlag()
        # 当前用户名不存在才可以执行
        if self.flag == False:
            self.Destroy()
            self.main_Frame.Show(True)
        else:
            self.user_ctrl.SetValue(u"请重新输入")
            self.password_ctrl.SetValue("")

    def OnCloseWindow(self, event):
        self.Destroy()
        self.main_Frame.Show(True)

if __name__ == "__main__":
    app = wx.App()
    frame = Register_Now_Frame(u"用户登录界面", 111)
    frame.Show(True)
    app.MainLoop()