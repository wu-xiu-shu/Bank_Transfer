#!/usr/bin/python
#coding: utf-8

"""
管理员操作界面
显示所有的账户以及账户的余额信息
"""

import wx
import wx.grid
import pymysql
from mysql_all_is_use import Mysql_All_is_Use

class All_User_Money_Frame(wx.Frame):
    def __init__(self, details):
        super(All_User_Money_Frame, self).__init__(None, -1, u"账户余额", size=(300, 200), pos=(400, 100),
                                      style=wx.DEFAULT_FRAME_STYLE ^ (
                                      wx.RESIZE_BORDER | wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX))
        self.details = details
        mygrid = MyGrid(self)

        self.Bind(wx.EVT_CLOSE, self.OnExit)

    def OnExit(self, event):
        self.Destroy()
        # 设置收支详情这个键可以点击
        self.details.Enable(True)

class MyGrid(wx.grid.Grid):
    def __init__(self, parent):
        super(MyGrid, self).__init__(parent, -1)

        lable_list = [u"用户名", u"账户金额"]
        # 用CreateGrid来实现，以网格的形式来显示
        conn = Mysql_All_is_Use()
        conn = conn.getConn()
        sql_select = "select username, money from bank_user;"
        cursor = conn.cursor()
        try:
            cursor.execute(sql_select)
            rs = cursor.fetchall()
            self.CreateGrid(len(rs), 2)
            for x, y in enumerate(lable_list):
                self.SetColLabelValue(x, y)

            for x, r in enumerate(rs):
                print x, r
                self.SetCellValue(x, 0, str(r[0]))
                self.SetCellValue(x, 1, str(r[1]))

        except Exception as e:
            print e
        finally:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    app = wx.App()
    frame = All_User_Money_Frame(111)
    frame.Show(True)
    app.MainLoop()