#!/usr/bin/python
#coding: utf-8

"""
管理员的操作界面
"""

import wx
import pymysql
from check_account import Check_Account_Frame
from all_user_money import All_User_Money_Frame
from delete_user_id import Delete_User_Id_Frame

class Admin_Frame(wx.Frame):
    def __init__(self, signin_Frame):
        super(Admin_Frame, self).__init__(None, -1, u"管理员界面", size=(300, 200), pos=(100, 100),
                                      style=wx.DEFAULT_FRAME_STYLE ^ (
                                      wx.RESIZE_BORDER | wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX))
        self.signin_Frame = signin_Frame
        self.CreateStatusBar()
        menubar = wx.MenuBar()
        menu1 = wx.Menu()
        self.all_user = menu1.Append(-1, u"查看账户", u"显示账户名")
        self.Bind(wx.EVT_MENU, self.All_User, self.all_user)
        self.all_user_money = menu1.Append(-1, u"账户余额", u"显示账户的余额和账户名")
        self.Bind(wx.EVT_MENU, self.All_User_Money, self.all_user_money)
        self.delete_user_id = menu1.Append(-1, u"删除账户", u"删除选中的账户")
        self.Bind(wx.EVT_MENU, self.Delete_User_Id, self.delete_user_id)
        menubar.Append(menu1, u"所有账户")
        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def All_User(self, event):
        "查看账户"
        user = Check_Account_Frame()

    def All_User_Money(self, event):
        "账户余额"
        user = All_User_Money_Frame(self.all_user_money)
        user.Show(True)
        self.all_user_money.Enable(False)

    def Delete_User_Id(self, event):
        "删除账户"
        user = Delete_User_Id_Frame(self.delete_user_id)
        user.Show(True)
        self.delete_user_id.Enable(False)

    def OnCloseWindow(self, event):
        self.Destroy()
        self.signin_Frame.Show(True)

if __name__ == "__main__":
    app = wx.App()
    frame = Admin_Frame(111)
    frame.Show(True)
    app.MainLoop()