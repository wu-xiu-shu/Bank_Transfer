#!/usr/bin/python
#coding: utf-8

"""
普通用户和管理员登录验证
"""

import wx
import pymysql
from mysql_all_is_use import Mysql_All_is_Use

# 注册验证
class Register_UserMysql():
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.flag = False

        conn = Mysql_All_is_Use()
        conn = conn.getConn()

        cursor = conn.cursor()
        sql_insert = "insert into bank_user(username, password) values('%s', '%s');" % (self.username, self.password)
        sql_select = "select username, password from bank_user;"
        try:
            cursor.execute(sql_select)
            rs = cursor.fetchall()
            for r in rs:
                if r[0] == self.username:
                    wx.MessageBox(u"当前用户名存在，请重新输入", u"错误信息", style=wx.OK)
                    self.flag = True
            if self.flag == False:
                # 上述操作没有问题则提交数据库
                cursor.execute(sql_insert)
                conn.commit()
        except Exception as e:
            print e
            # 出错的话数据库回滚
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

    def GetFlag(self):
        return self.flag

# 登录框
class Enter_UseMysql():
    def __init__(self, username, password, flag):
        self.username = username
        self.password = password
        self.flag = flag
        self.f = True

        conn = Mysql_All_is_Use()
        conn = conn.getConn()

        cursor = conn.cursor()
        if self.flag == True:   # 证明是普通用户
            sql = "select username, password from bank_user;"
        else:
            sql = "select username, password from bank_manager;"
        self.flag = False
        try:
            cursor.execute(sql)
            rs = cursor.fetchall()
            # print rs
            for r in rs:
                if r[0] == self.username and r[1] == self.password:
                    self.flag = True
                    self.SetFlag(True)
                    break
            if self.flag == False:
                wx.MessageBox(u"用户名或者密码输入错误", u"错误信息", style=wx.OK)
                self.SetFlag(False)
        except Exception as e:
            print e
        finally:
            cursor.close()
            conn.close()

    def GetUserName(self):
        # 登录成功
        if self.flag == True:
            return self.username
        else:
            return None

    def SetFlag(self, flag):
        self.f = flag

    def GetFlag(self):
        return self.f