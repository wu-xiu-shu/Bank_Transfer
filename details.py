#!/usr/bin/python
#coding: utf-8

"""
普通用户操作界面
查看收支详情
"""

import wx
import math
import wx.grid
import pymysql
from mysql_all_is_use import Mysql_All_is_Use

class Details_Frame(wx.Frame):
    def __init__(self, details, label):
        super(Details_Frame, self).__init__(None, -1, label, size=(400, 200), pos=(400, 100),
                                      style=wx.DEFAULT_FRAME_STYLE ^ (
                                      wx.RESIZE_BORDER | wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX))
        self.details = details
        self.label = label

        sql_select1 = "select username from bank_user where bool_id = 1;"
        # 银行转账的情况
        sql_select2 = "select username, money, receive_username, time_operate from some_operation;"
        # 他人转账时收入的情况
        sql_select3 = "select username, money, receive_username, time_operate from some_operation where money >= 0;"
        # 转出的情况
        sql_select4 = "select username, money, receive_username, time_operate from some_operation where money <= 0;"

        conn = Mysql_All_is_Use()
        conn = conn.getConn()
        cur = conn.cursor()
        try:
            # 首先获取操作的用户名
            cur.execute(sql_select1)
            rs = cur.fetchall()
            # 获得用户名
            rs = rs[0][0]
            # print rs
            # print self.label

            if self.label == u"银行转账":
                cur.execute(sql_select2)
                all_rs = cur.fetchall()
                # print all_rs
                the_all = []
                for r in all_rs:
                    # print r
                    # print r[2]
                    if r[2] is None:
                        s = (r[0], r[1], r[3])
                        the_all.append(s)
                # print the_all
                label_list = [u"用户名", u"银行转账", u"操作时间"]
                MyGrid(self, the_all, rs, label_list)

            elif self.label == u"转出的钱":
                cur.execute(sql_select4)
                all_rs = cur.fetchall()
                the_all = []
                for r in all_rs:
                    # print r
                    if r[0] == rs and r[2] is not None:
                        s = (r[2], r[1], r[3])
                        the_all.append(s)
                label_list = [u"转出账户", u"转出的钱", u"操作时间"]
                MyGrid(self, the_all, rs, label_list)
            else:
                cur.execute(sql_select3)
                all_rs = cur.fetchall()
                the_all = []
                for r in all_rs:
                    # print r
                    if r[0] == rs and r[2] is not None:
                        s = (r[2], r[1], r[3])
                        the_all.append(s)

                label_list = [u"转入账户", u"转入金额", u"操作时间"]
                MyGrid(self, the_all, rs, label_list)

        except Exception as e:
            print e
        finally:
            cur.close()
            conn.close()

        self.Bind(wx.EVT_CLOSE, self.OnExit)

    def OnExit(self, event):
        self.Destroy()
        # 设置收支详情这个键可以点击
        self.details.Enable(True)

class MyGrid(wx.grid.Grid):
    def __init__(self, parent, all_rs, rs, label_list):
        super(MyGrid, self).__init__(parent, -1)
        self.all_rs = all_rs
        self.rs = rs
        self.label_list = label_list

        try:
            self.CreateGrid(len(all_rs), 3)
            for x, y in enumerate(self.label_list):
                self.SetColLabelValue(x, y)

            for x, r in enumerate(all_rs):
                # print x, r
                self.SetCellValue(x, 0, r[0])
                self.SetCellValue(x, 1, str(r[1]))
                self.SetCellValue(x, 2, str(r[2]))
        except Exception as e:
            print e
        finally:
            pass

if __name__ == "__main__":
    app = wx.App()
    frame = Details_Frame(111, u"收支详情")
    frame.Show(True)
    app.MainLoop()