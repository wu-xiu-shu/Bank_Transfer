#!/usr/bin/python
#coding: utf-8

import pymysql

class Mysql_All_is_Use():

    def __init__(self):
        # 连接数据库
        self.conn = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            passwd='root',
            db='bank_operation',
            charset='utf8',
        )

    def getConn(self):
        return self.conn