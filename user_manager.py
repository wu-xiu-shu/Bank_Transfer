#!/usr/bin/python
#coding: utf-8

import wx
import pymysql
from balance import Balance_Frame
from details import Details_Frame
from ouput_accounts import Ouput_Accounts_Frame
from input_accounts import Input_Accounts_Frame
from mysql_all_is_use import Mysql_All_is_Use

class User_Frame(wx.Frame):
    def __init__(self, signin_Frame):
        super(User_Frame, self).__init__(None, -1, u"用户操作中心", size=(300, 200), pos=(100, 100),
                                      style=wx.DEFAULT_FRAME_STYLE ^ (
                                          wx.RESIZE_BORDER | wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX))
        self.signin_Frame = signin_Frame
        self.CreateStatusBar()
        panel = wx.Panel(self, -1)

        submenu = wx.Menu()
        self.submenu1 = submenu.Append(-1, u"收到的钱")
        self.Bind(wx.EVT_MENU, self.SubMenu1, self.submenu1)
        self.submenu2 = submenu.Append(-1, u"转出的钱")
        self.Bind(wx.EVT_MENU, self.SubMenu2, self.submenu2)
        self.submenu3 = submenu.Append(-1, u"银行转入")
        self.Bind(wx.EVT_MENU, self.SubMenu3, self.submenu3)

        menubar = wx.MenuBar()
        menu1 = wx.Menu()
        self.input_accounts = menu1.Append(-1, u"&转入", u"用户收入的钱")
        self.Bind(wx.EVT_MENU, self.Input_Accounts, self.input_accounts)
        self.output_accounts = menu1.Append(-1, u"&转出", u"用户转出的钱")
        self.Bind(wx.EVT_MENU, self.Output_Accounts, self.output_accounts)
        self.details = menu1.AppendMenu(-1, u"&收支详情", submenu)

        menubar.Append(menu1, u"转账信息")
        menu2 = wx.Menu()
        self.all_balance = menu2.Append(-1, u"&查询余额", u"用户所剩余的钱数")
        self.Bind(wx.EVT_MENU, self.All_Balance, self.all_balance)
        menubar.Append(menu2, u"账户余额")
        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def SubMenu3(self, event):
        "银行转账"
        self._details = Details_Frame(self.submenu3, u"银行转账")
        self._details.Show(True)
        self.submenu3.Enable(False)

    def SubMenu2(self, event):
        "转出的钱"
        self.__details = Details_Frame(self.submenu2, u"转出的钱")
        self.__details.Show(True)
        self.submenu2.Enable(False)

    def SubMenu1(self, event):
        "接收的钱"
        self.___details = Details_Frame(self.submenu1, u"接收的钱")
        self.___details.Show(True)
        self.submenu1.Enable(False)

    def All_Balance(self, event):
        "账户余额信息"
        self._balance = Balance_Frame(self.all_balance)
        self._balance.Show(True)
        # 设置此按钮只能够点击一次
        self.all_balance.Enable(False)

    def Output_Accounts(self, event):
        "转出的钱数"
        self._accounts = Ouput_Accounts_Frame(self.output_accounts)
        self._accounts.Show(True)

        self.output_accounts.Enable(False)

    def Input_Accounts(self, event):
        "转入的钱数,从银行转入"
        self.__accounts = Input_Accounts_Frame(self.input_accounts)
        self.__accounts.Show(True)
        self.input_accounts.Enable(False)

    def OnCloseWindow(self, event):
        "如果进行关闭的时候，把bool_id重新修改为0，因为等于1是正在进行的操作"

        # self._accounts.Close(True)
        # self.__accounts.Close(True)
        # self._balance.Close(True)
        # self._details.Close(True)
        # self.___details.Close(True)
        # self.___details.Close(True)

        conn = Mysql_All_is_Use()
        conn = conn.getConn()
        sql_update = sql_update = "update bank_user set bool_id = 0 where bool_id != 0;"
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
        self.Destroy()
        self.signin_Frame.Show(True)

if __name__ == "__main__":
    app = wx.App()
    frame = User_Frame(111)
    frame.Show(True)
    app.MainLoop()