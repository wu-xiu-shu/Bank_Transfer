#!/usr/bin/python
#coding: utf-8

"""
普通用户的操作界面
显示用户收入的信息
"""

import wx
from mysql_all_is_use import Mysql_All_is_Use

class Input_Accounts_Frame(wx.Frame):
    def __init__(self, input_accounts):
        super(Input_Accounts_Frame, self).__init__(None, -1, u"收支详情", size=(300, 200), pos=(400, 100),
                                      style=wx.DEFAULT_FRAME_STYLE ^ (
                                      wx.RESIZE_BORDER | wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX))
        self.input_accounts = input_accounts
        panel = wx.Panel(self, -1)

        topLbl = wx.StaticText(panel, -1, u"此次从银行要转入的钱数", style=wx.ALIGN_LEFT)
        topLbl.SetFont(wx.Font(13, wx.SWISS, wx.NORMAL, wx.BOLD))
        user = wx.StaticText(panel, -1, u"转入金额:")
        self.user_ctrl = wx.TextCtrl(panel, -1, u"输入要转入的钱数")

        self.btn1 = wx.Button(panel, -1, u"确认转入")
        self.Bind(wx.EVT_BUTTON, self.OnButton_1, self.btn1)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(topLbl, 0, wx.ALL, 5)
        mainSizer.Add(wx.StaticLine(panel), 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)

        addSizer = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)
        addSizer.AddGrowableCol(1)
        addSizer.Add(user, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addSizer.Add(self.user_ctrl, 0, wx.EXPAND)
        addSizer.Add((10, 10))
        addSizer.Add(self.btn1, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)

        mainSizer.Add(addSizer, 0, wx.EXPAND | wx.ALL, 10)
        panel.SetSizer(mainSizer)

        self.Bind(wx.EVT_CLOSE, self.OnExit)

    def OnButton_1(self, event):
        "修改两个数据库，一个是bank_user，一个是some_operation"
        conn = Mysql_All_is_Use()
        conn = conn.getConn()
        sql_select1 = "select username from bank_user where bool_id = 1;"
        sql_update1 = "update bank_user set money = money + %d where bool_id = 1;"
        sql_insert2 = "insert into some_operation(username, money) values('%s', %d);"
        cur = conn.cursor()
        try:
            # 输入的钱数
            the_money = int(self.user_ctrl.GetValue())
            st = sql_update1 % the_money
            cur.execute(st)
            cur.execute(sql_select1)
            rs = cur.fetchall()
            username = rs[0][0]
            # print(username)
            st = sql_insert2 % (username, the_money)
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
        self.input_accounts.Enable(True)

    def OnExit(self, event):
        self.Destroy()
        # 设置此按钮只能够点击一次
        self.input_accounts.Enable(True)

if __name__ == "__main__":
    app = wx.App()
    frame = Input_Accounts_Frame(111)
    frame.Show(True)
    app.MainLoop()