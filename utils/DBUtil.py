#! /usr/bin/python3
# -*- coding: utf8 -*-
import pymysql
from utils.ConfigUtil import ConfigUtil
from utils.Constant import Constant


class DBUtil:
    # 连接MySQL数据库方法
    def __init__(self):
        config = ConfigUtil()
        self.dbhost   = config.getDB(Constant.CONFIG_PARAM_DB_HOST)
        self.port     = config.getDB(Constant.CONFIG_PARAM_DB_PORT)
        self.database = config.getDB(Constant.CONFIG_PARAM_DB_DATABASE)
        self.username = config.getDB(Constant.CONFIG_PARAM_DB_USERNAME)
        self.password = config.getDB(Constant.CONFIG_PARAM_DB_PASSWORD)
    
    def connectDB(self,*args):
        if args.__len__() == 0 :
            pass
        else:
            self.dbhost   = args[0]
            self.database = args[1]
            self.username = args[2]
            self.password = args[3]
        return pymysql.connect(host=self.dbhost, user=self.username, passwd=self.password, db=self.database,charset=Constant.CHAR_SET_DB)
    
    def executeSQL(self,connection,sql):
        try:
            connection.cursor().execute(sql)
            connection.commit()
        except Exception as e:
            print("Error",str(e),sql)
    
    def insertSQL(self,connection,sql,values):
        try:
            connection.cursor().executemany(sql,values)
            connection.commit()
        except Exception as e:
            print("Error",str(e),sql)
    
    
    def fetchAll(self,connection,sql):
        cursor = connection.cursor()
        cursor.execute(sql)
        return cursor.fetchall()
    
    def fetchAlltoList(self,connection,sql,column):
        values = []
        records = self.fetchAll(connection,sql)
        for record in records:
            # get all columns
            if column == -1:
                temp = []
                for i in range(len(record)):
                    if record[i] == None:
                        temp.append("")
                    else:
                        temp.append(str(record[i]))
                values.append(temp)
            else:
                values.append(record[column])
        return values
    
    def fetchOne(self,connection,sql):
        cursor = connection.cursor()
        cursor.execute(sql)
        return cursor.fetchone()
            
    def closeDB(self,connection):
        connection.close()
