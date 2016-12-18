#!/usr/bin/python
#coding: utf-8

"""
普通用户的操作界面
查看账户余额
"""

import wx
import pymysql
from mysql_all_is_use import Mysql_All_is_Use
from signin_user_mysql import Enter_UseMysql

class Balance_Frame(wx.Frame):
    def __init__(self, all_balance):
        super(Balance_Frame, self).__init__(None, -1, u"账户余额", size=(300, 200), pos=(400, 100),
                                      style=wx.DEFAULT_FRAME_STYLE ^ (
                                      wx.RESIZE_BORDER | wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX))
        self.all_balance = all_balance
        panel = wx.Panel(self, -1)

        topLbl = wx.StaticText(panel, -1, u"用户剩余钱数")
        topLbl.SetFont(wx.Font(13, wx.SWISS, wx.NORMAL, wx.BOLD))
        text1 = wx.StaticText(panel, -1, u"账户余额:")
        self.text1_ctrl = wx.TextCtrl(panel, -1,"")
        self.text1_ctrl.Enable(False)

        conn = Mysql_All_is_Use()
        conn = conn.getConn()
        cursor = conn.cursor()
        # 已经登录成功后，用户名肯定存在，此时直接查看钱数
        sql = "select username, money, bool_id from bank_user;"
        try:
            cursor.execute(sql)
            rs = cursor.fetchall()
            for r in rs:
                if int(r[2]) == 1:
                    self.text1_ctrl.SetValue(u"%d元" % r[1])
                    break
        except Exception as e:
            print e
        finally:
            cursor.close()
            conn.close()

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(topLbl, 0, wx.ALL, 5)
        mainSizer.Add(wx.StaticLine(panel), 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)

        addSizer = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)
        addSizer.AddGrowableCol(1)
        addSizer.Add(text1, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addSizer.Add(self.text1_ctrl, 0, wx.EXPAND)
        mainSizer.Add(addSizer, 0, wx.EXPAND|wx.ALL, 10)
        panel.SetSizer(mainSizer)

        self.Bind(wx.EVT_CLOSE, self.OnExit)

    def OnExit(self, event):
        self.Destroy()
        # 设置查询余额可以再次被点击
        self.all_balance.Enable(True)

if __name__ == "__main__":
    app = wx.App()
    frame = Balance_Frame(111)
    frame.Show(True)
    app.MainLoop()