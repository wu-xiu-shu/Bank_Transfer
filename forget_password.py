#!/usr/bin/python
#coding: utf-8

"""
忘记密码的操作界面
"""

import wx
import pymysql
from mysql_all_is_use import Mysql_All_is_Use

class Forget_Password_Frame(wx.Frame):
    def __init__(self, main_Frame):
        super(Forget_Password_Frame, self).__init__(None, -1, u"密码查找界面", size=(300, 200), pos=(100, 100),
                                         style=wx.DEFAULT_FRAME_STYLE ^ (
                                             wx.RESIZE_BORDER | wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX))
        self.main_Frame = main_Frame
        self.panel = wx.Panel(self, -1)
        topLbl = wx.StaticText(self.panel, -1, u"查找密码界面")
        topLbl.SetFont(wx.Font(13, wx.SWISS, wx.NORMAL, wx.BOLD))
        user = wx.StaticText(self.panel, -1, u"用户名:")
        self.user_ctrl = wx.TextCtrl(self.panel, -1, u"输入用户名")

        btn1 = wx.Button(self.panel, -1, u"查找密码")
        self.Bind(wx.EVT_BUTTON, self.OnButton_1, btn1)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(topLbl, 0, wx.ALL, 5)
        mainSizer.Add(wx.StaticLine(self.panel), 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)

        addSizer = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)
        addSizer.AddGrowableCol(1)
        addSizer.Add(user, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addSizer.Add(self.user_ctrl, 0, wx.EXPAND)
        addSizer.Add((10, 10))
        addSizer.Add(btn1, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)

        mainSizer.Add(addSizer, 0, wx.EXPAND | wx.ALL, 10)
        self.panel.SetSizer(mainSizer)

        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def OnButton_1(self, event):

        conn = Mysql_All_is_Use()
        conn = conn.getConn()
        cursor = conn.cursor()
        sql = "select username, password from bank_user;"
        try:
            cursor.execute(sql)
            rs = cursor.fetchall()
            flag = False
            for r in rs:
                if r[0] == self.user_ctrl.GetValue():
                    wx.MessageBox("%s" % r[1], u"所得密码如下", wx.OK)
                    flag = True
                    break
            if flag == False:
                wx.MessageBox(u"当前用户名不存在", u"错误信息", style = wx.OK)
        except Exception as e:
            print(self.__doc__)
            print e
        finally:
            cursor.close()
            conn.close()

    def OnCloseWindow(self, event):
        self.Destroy()
        self.main_Frame.Show(True)

if __name__ == "__main__":
    app = wx.App()
    frame = Forget_Password_Frame(111)
    frame.Show(True)
    app.MainLoop()