#!/usr/bin/python
#coding: utf-8

"""
所有程序运行的主界面
"""

import wx
from signin import Enter_User
import pymysql

class MyFrame(wx.Frame):
    def __init__(self):
        super(MyFrame, self).__init__(None, -1, u"银行转账模拟", size=(300, 200), pos=(100, 100),
                                      style=wx.DEFAULT_FRAME_STYLE ^ (
                                      wx.RESIZE_BORDER | wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX))
        self.panel = wx.Panel(self, -1)
        # 创建一个状态栏
        self.CreateStatusBar()
        menubar = wx.MenuBar()
        menu = wx.Menu()
        self.administrators = menu.Append(-1, u"管理员登录", u"后台管理者登录所选择界面")
        self.Bind(wx.EVT_MENU, self.SignInAdmin, self.administrators)
        self.users = menu.Append(-1, u"用户登录", u"普通用户登录界面")
        self.Bind(wx.EVT_MENU, self.SignInUser, self.users)
        menu.AppendSeparator()
        self.exit = menu.Append(-1, u"&Exit", u"退出系统")
        self.Bind(wx.EVT_MENU, self.OnExit, self.exit)
        menubar.Append(menu, u"登录类型")
        menu = wx.Menu()
        m = menu.Append(-1, u"&代码手", u"作者简介")
        self.Bind(wx.EVT_MENU, self.OnAbout, m)
        menubar.Append(menu, u"&关于")
        self.SetMenuBar(menubar)

    def OnAbout(self, event):
        wx.MessageBox(u"作者: 吴修树\n开发时间：2016/12/18", u"简介", style=wx.OK)

    def SignInUser(self, event):
        enter_user = Enter_User(u"用户登录界面", self)
        enter_user.Show(True)
        self.Show(False)

    def SignInAdmin(self, event):
        enter_user = Enter_User(u"管理员登录界面", self)
        enter_user.Show(True)
        self.Show(False)

    def OnExit(self, event):
        self.Close(True)

if __name__ == "__main__":
    app = wx.App()
    frame = MyFrame()
    frame.Show(True)
    app.MainLoop()