#!/usr/bin/python
#coding: utf-8

"""
管理员操作界面
删除指定的账户
删除成功弹出对话框
如果删除失败输出错误信息
"""

import wx
import pymysql
from mysql_all_is_use import Mysql_All_is_Use

class Delete_User_Id_Frame(wx.Frame):
    def __init__(self, details):
        super(Delete_User_Id_Frame, self).__init__(None, -1, u"账户余额", size=(300, 200), pos=(400, 100),
                                      style=wx.DEFAULT_FRAME_STYLE ^ (
                                      wx.RESIZE_BORDER | wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX))
        self.details = details
        panel = wx.Panel(self, -1)

        topLbl = wx.StaticText(panel, -1, u"删除输入用户")
        topLbl.SetFont(wx.Font(13, wx.SWISS, wx.NORMAL, wx.BOLD))
        text1 = wx.StaticText(panel, -1, u"用户名:")
        self.text1_ctrl = wx.TextCtrl(panel, -1, )
        btn1 = wx.Button(panel, -1, u"删除用户")
        self.Bind(wx.EVT_BUTTON, self.OnButton, btn1)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(topLbl, 0, wx.ALL, 5)
        mainSizer.Add(wx.StaticLine(panel), 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)

        addSizer = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)
        addSizer.AddGrowableCol(1)
        addSizer.Add(text1, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addSizer.Add(self.text1_ctrl, 0, wx.EXPAND)
        addSizer.Add((10, 10))
        addSizer.Add(btn1, 0, wx.EXPAND)
        mainSizer.Add(addSizer, 0, wx.EXPAND | wx.ALL, 10)
        panel.SetSizer(mainSizer)

        self.Bind(wx.EVT_CLOSE, self.OnExit)

    def OnButton(self, event):
        "实现点击的时候删除账户的功能"
        conn = Mysql_All_is_Use()
        conn = conn.getConn()
        print(self.text1_ctrl.GetValue())
        sql_delete = "delete from bank_user where username = '%s';" % self.text1_ctrl.GetValue()
        sql_select = "select username from bank_user;"
        cur = conn.cursor()
        try:
            cur.execute(sql_select)
            self.rs1 = cur.fetchall()

            cur.execute(sql_delete)
            conn.commit()
        except Exception as e:
            print e
        finally:
            cur.execute(sql_select)
            rs2 = cur.fetchall()
            if len(self.rs1) == len(rs2) + 1:
                wx.MessageBox(u"删除成功", u"删除结果", style=wx.OK)
            else:
                wx.MessageBox(u"删除失败", u"删除结果", style=wx.OK)
            cur.close()
            conn.close()

    def OnExit(self, event):
        self.Destroy()
        # 设置收支详情这个键可以点击
        self.details.Enable(True)

if __name__ == "__main__":
    app = wx.App()
    frame = Delete_User_Id_Frame(111)
    frame.Show(True)
    app.MainLoop()