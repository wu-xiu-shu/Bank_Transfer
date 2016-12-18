#!/usr/bin/python
#coding: utf-8

"""
管理者操作界面
查看账户的余额
"""

import wx
import wx.grid
import pymysql
from mysql_all_is_use import Mysql_All_is_Use

class Check_Account_Frame():
    def __init__(self):
        dlg = wx.TextEntryDialog(None, u"请输入要查找账户:", u"查找账户", u"")
        if dlg.ShowModal() == wx.ID_OK:
            conn = Mysql_All_is_Use()
            conn = conn.getConn()
            cur = conn.cursor()
            sql_select = "select username, money from bank_user;"
            try:
                cur.execute(sql_select)
                rs = cur.fetchall()
                flag = False
                for r in rs:
                    if r[0] == dlg.GetValue():
                        wx.MessageBox(u"用户的钱数为：%d元" % r[1], u"查询结果", style = wx.OK)
                        flag = True
                        break
                if flag == False:
                    wx.MessageBox(u"当前用户名不存在", u"查询结果", style = wx.OK)
            except Exception as e:
                print e
            finally:
                cur.close()
                conn.close()

if __name__ == "__main__":
    app = wx.App()
    frame = Check_Account_Frame(111)
    app.MainLoop()