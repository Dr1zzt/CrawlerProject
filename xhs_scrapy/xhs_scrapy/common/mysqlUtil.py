#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   mysqlUtil.py
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/4/7 14:24   Drizzt      1.0         None
"""
import pymysql


class MysqlConn:
    def __init__(self):
        self.host = ""
        self.port = 3306
        self.user = "root"
        self.passwd = ""
        self.db = ""

    def connect(self):
        connect = pymysql.connect(
            host=self.host,
            port=self.port,
            db=self.db,
            user=self.user,
            passwd=self.passwd,
            use_unicode=True)
        return connect

    def process_item(self, sql, re=False):
        """
        数据库连接
        :param re:
        :param sql: sql语句
        :return:
        """
        connect = self.connect()
        if re:
            try:
                cursor = connect.cursor()
                cursor.execute(sql)
                result = cursor.fetchall()
                cursor.close()
                connect.close()
                return result
            except RuntimeError as error:
                connect.rollback()
                print(sql)
                raise error
        else:
            try:
                cursor = connect.cursor()
                cursor.execute(sql)
                connect.commit()
                cursor.close()
                connect.close()
            except RuntimeError as error:
                connect.rollback()
                print(sql)
                raise error
