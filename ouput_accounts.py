#!/usr/bin/python
#coding: utf-8

"""
普通用户操作界面
查看转出的信息
"""

import wx
import pymysql
from mysql_all_is_use import Mysql_All_is_Use

class Ouput_Accounts_Frame(wx.Frame):
    "用户转出相应的金额，要满足所转的钱数不大于现在已有的钱数,转入的账户存在"
    def __init__(self, ouput_accounts):
        super(Ouput_Accounts_Frame, self).__init__(None, -1, u"金钱转出", size=(300, 200), pos=(400, 100),
                                      style=wx.DEFAULT_FRAME_STYLE ^ (
                                      wx.RESIZE_BORDER | wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX))
        self.ouput_accounts = ouput_accounts
        panel = wx.Panel(self, -1)

        topLbl = wx.StaticText(panel, -1, u"请输入转出金额及接受用户", style = wx.ALIGN_LEFT)
        topLbl.SetFont(wx.Font(13, wx.SWISS, wx.NORMAL, wx.BOLD))
        user = wx.StaticText(panel, -1, u"转出金额:")
        self.user_ctrl = wx.TextCtrl(panel, -1, u"输入转出金额")
        receive_username = wx.StaticText(panel, -1, u"接收账户:")
        self.receive_username = wx.TextCtrl(panel, -1, u"接收账户的用户名")

        self.btn1 = wx.Button(panel, -1, u"确认转出")
        self.Bind(wx.EVT_BUTTON, self.OnButton_1, self.btn1)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(topLbl, 0, wx.ALL, 5)
        mainSizer.Add(wx.StaticLine(panel), 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)

        addSizer = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)
        addSizer.AddGrowableCol(1)
        addSizer.Add(user, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addSizer.Add(self.user_ctrl, 0, wx.EXPAND)

        addSizer.Add(receive_username, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addSizer.Add(self.receive_username, 0, wx.EXPAND)
        addSizer.Add((10, 10))
        addSizer.Add(self.btn1, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)

        mainSizer.Add(addSizer, 0, wx.EXPAND | wx.ALL, 10)
        panel.SetSizer(mainSizer)

        self.Bind(wx.EVT_CLOSE, self.OnExit)

    def OnButton_1(self, event):
        sql_select1 = "select username, money from bank_user where bool_id = 1;"
        sql_update1 = "update bank_user set money = money %c %d where username = '%s';"
        sql_insert2 = "insert into some_operation(username, money, receive_username) values('%s', %d, '%s');"
        conn = Mysql_All_is_Use()
        conn = conn.getConn()
        cur = conn.cursor()
        try:
            cur.execute(sql_select1)
            rs1 = cur.fetchall()
            # 返回的是一个元祖，而表示每一个数据的也是元组，所以用二维
            username = rs1[0][0]
            true_money = int(rs1[0][1])
            # 转账的钱数
            the_money = int(self.user_ctrl.GetValue())
            receive_username = self.receive_username.GetValue()
            print(username, the_money, receive_username)
            if(the_money > true_money):
                self.user_ctrl.SetValue(u"请重新输入金额")
                wx.MessageBox(u"转账金额大于现有钱数", u"错误信息", style = wx.OK)
            else:
                st = sql_insert2 % (username, -the_money, receive_username)
                cur.execute(st)
                st = sql_insert2 % (receive_username, the_money, username)
                cur.execute(st)
                st = sql_update1 % ('-', the_money, username)
                cur.execute(st)
                st = sql_update1 % ('+', the_money, receive_username)
                cur.execute(st)

            conn.commit()
        except Exception as e:
            print e
            conn.rollback()
        finally:
            cur.close()
            conn.close()

        # 点击确定以后就及时关闭该窗口，防止多次点击
        self.Destroy()
        self.ouput_accounts.Enable(True)

    def OnExit(self, event):
        self.Destroy()
        self.ouput_accounts.Enable(True)

if __name__ == "__main__":
    app = wx.App()
    frame = Ouput_Accounts_Frame(111)
    frame.Show(True)
    app.MainLoop()