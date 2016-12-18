#!/usr/bin/python
#coding: utf-8

"""
管理员和普通用户的登录界面
"""

import wx
import pymysql
from user_manager import User_Frame
from admin_manager import Admin_Frame
from signin_user_mysql import Register_UserMysql, Enter_UseMysql
from register_now import Register_Now_Frame
from forget_password import Forget_Password_Frame
from mysql_all_is_use import Mysql_All_is_Use

class Enter_User(wx.Frame):
    def __init__(self, label, main_Frame):
        super(Enter_User, self).__init__(None, -1, label, size=(300, 200), pos=(100, 100),
                                      style=wx.DEFAULT_FRAME_STYLE ^ (
                                          wx.RESIZE_BORDER | wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX))
        self.main_Frame = main_Frame
        self.get_username = None
        self.panel = wx.Panel(self, -1)
        topLbl = wx.StaticText(self.panel, -1, u"请确认用户名和密码再登录")
        topLbl.SetFont(wx.Font(13, wx.SWISS, wx.NORMAL, wx.BOLD))
        user = wx.StaticText(self.panel, -1, u"用户名:")
        self.user_ctrl = wx.TextCtrl(self.panel, -1, u"输入用户名")
        password = wx.StaticText(self.panel, -1, u"密  码:")
        self.password_ctrl = wx.TextCtrl(self.panel, -1, "", style = wx.TE_PASSWORD)

        self.btn1 = wx.Button(self.panel, -1, u"立即注册")
        self.Bind(wx.EVT_BUTTON, self.OnButton_1, self.btn1)
        self.btn2 = wx.Button(self.panel, -1, u"忘记密码")
        self.Bind(wx.EVT_BUTTON, self.OnButton_2, self.btn2)
        btn3 = wx.Button(self.panel, -1, u"用户登录")
        self.Bind(wx.EVT_BUTTON, self.OnButton_3, btn3)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(topLbl, 0, wx.ALL, 5)
        mainSizer.Add(wx.StaticLine(self.panel), 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 5)

        addSizer = wx.FlexGridSizer(cols = 3, hgap = 5, vgap = 5)
        addSizer.AddGrowableCol(1)
        addSizer.Add(user, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        addSizer.Add(self.user_ctrl, 0, wx.EXPAND)
        addSizer.Add(self.btn1, 0, wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        addSizer.Add(password, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        addSizer.Add(self.password_ctrl, 0, wx.EXPAND)
        addSizer.Add(self.btn2, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
        addSizer.Add((50, 50))
        addSizer.Add(btn3, 0, wx.EXPAND)

        mainSizer.Add(addSizer, 0, wx.EXPAND|wx.ALL, 10)
        self.panel.SetSizer(mainSizer)

        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def GetUserName(self):
        return self.get_username

    def OnButton_1(self, event):
        "用户注册界面"
        st = self.GetTitle()
        if st != u"用户登录界面":
            self.btn1.Enable(False)
            return
        win = Register_Now_Frame(self)
        win.Show(True)
        self.Show(False)

    def OnButton_2(self, event):
        "由于管理员的特殊权限，所以管理员不对忘记密码进行讨论"
        st = self.GetTitle()
        if st != u"用户登录界面":
            self.btn2.Enable(False)
            return
        win = Forget_Password_Frame(self)
        win.Show(True)
        self.Show(False)

    def OnButton_3(self, event):
        "用户登录界面"
        st = self.GetTitle()
        username = self.user_ctrl.GetValue()
        password = self.password_ctrl.GetValue()

        if st == u"用户登录界面":
            users = User_Frame(self)
            rs = Enter_UseMysql(username, password, True)
            if rs.GetFlag() == False: # 登录不成功
                return
            # 登录成功获取登录的用户名
            # 如果登录成功，则把当前列的bool_id修改为1
            conn = Mysql_All_is_Use()
            conn = conn.getConn()
            sql_update = sql_update = "update bank_user set bool_id = 1 where username = '%s';"%(username)
            cursor = conn.cursor()
            try:
                cursor.execute(sql_update)
                conn.commit()
            except Exception as e:
                print e
                conn.rollback()
            finally:
                cursor.close()
                conn.close()

            self.get_username = username
            users.Show(True)
            self.Show(False)
        else:
            admin = Admin_Frame(self)
            rs = Enter_UseMysql(username, password, False)
            if rs.GetFlag() == False:
                return
            admin.Show(True)
            self.Show(False)

    def OnCloseWindow(self, event):
        self.Destroy()
        self.main_Frame.Show(True)

if __name__ == "__main__":
    app = wx.App()
    frame = Enter_User(u"用户登录界面", 111)
    frame.Show(True)
    app.MainLoop()