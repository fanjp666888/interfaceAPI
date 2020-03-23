#! /usr/bin/python3
# -*- coding: utf8 -*-
import codecs
import configparser
import os
from utils.Constant import Constant


class ConfigUtil:    
    def __new__(cls):
        """创建读取配置文件的单例"""
        if not hasattr(cls, 'instance'):
            cls.instance = super(ConfigUtil, cls).__new__(cls)
        return cls.instance
    
    def __init__(self):
        proDir = os.path.join(os.getcwd(), Constant.PATH_FOR_CONF)  # 动态获取配置文件目录相对路径
        print(os.getcwd())
        configPath = os.path.join(proDir, Constant.CONFIG_FILE_NAME)  # 动态获取配置文件ini的相对路径
        self.removeUTFBom(configPath)
        self.cf = configparser.ConfigParser()  # 将所有的配置文件读取并存储到变量self.cf中
        self.cf.read(configPath)

    def removeUTFBom(self, file):
        """Remove UTF-8的BOM,注：带BOM的会显示乱码"""
        configfile = open(file)
        data = configfile.read()
        if data[:3] == codecs.BOM_UTF8:
            data = data[3:]
            file = codecs.open(file, "w")
            file.write(data)
            file.close()
        configfile.close()
        
    def getInstance(self):
        if self.instance:
            return self.instance
        else:
            self.init(self)
            return self.instance
        
    def getSuningPrd(self, name):
        """读取Suning-prd配置信息"""
        value = self.cf.get(Constant.CONFIG_PARAM_SUNING_PRD, name)
        return value

    def getSuningSit(self, name):
        """读取Suning-sit配置信息"""
        value = self.cf.get(Constant.CONFIG_PARAM_SUNING_SIT, name)
        return value

    def getEnvironment(self, name):
        """读取测试配置信息"""
        value = self.cf.get(Constant.CONFIG_PARAM_ENV, name)
        return value
    
    def getDB(self, name):
        """读取数据库配置信息"""
        value = self.cf.get(Constant.CONFIG_PARAM_DB, name)
        return value
    
    def getRun(self, name):
        """读取测试配置信息"""
        value = self.cf.get(Constant.CONFIG_PARAM_RUN, name)
        return value
    
    def getSearch_SuningPrd(self):
        return self.getSuningPrd(Constant.CONFIG_PARAM_SUNING_PRD_SEARCH) 
    
    def getList_SuningPrd(self):
        return self.getSuningPrd(Constant.CONFIG_PARAM_SUNING_PRD_LIST)
              
    def getSearch_SuningSit(self):
        return self.getSuningSit(Constant.CONFIG_PARAM_SUNING_SIT_SEARCH) 
    
    def getList_SuningSit(self):
        return self.getSuningSit(Constant.CONFIG_PARAM_SUNING_SIT_LIST)
    
    def getSearch_SuningPre(self):
        return self.getSuningPre(Constant.CONFIG_PARAM_SUNING_PRE_SEARCH)

    def getList_SuningPre(self):
        return self.getSuningPre(Constant.CONFIG_PARAM_SUNING_PRE_LIST)

    def getSearch_SuningGray(self):
        return self.getSuningGray(Constant.CONFIG_PARAM_SUNING_GRAY_SEARCH)

    def getList_SuningGray(self):
        return self.getSuningGray(Constant.CONFIG_PARAM_SUNING_GRAY_LIST)
      
    def getSelectedEnvironment(self):
        """获取selected environment"""
        if self.getEnvironment(Constant.CONFIG_PARAM_ENV_PRD).lower() == "true":
            return (self.getSearch_SuningPrd(),self.getList_SuningPrd())
        
        if self.getEnvironment(Constant.CONFIG_PARAM_ENV_SIT).lower() == "true":
            return (self.getSearch_SuningSit(),self.getList_SuningSit())
        
        if self.getEnvironment(Constant.CONFIG_PARAM_ENV_PRE).lower() == "true":
            return (self.getSearch_SuningPre(),self.getList_SuningPre())
        
        if self.getEnvironment(Constant.CONFIG_PARAM_ENV_GRAY).lower() == "true":
            return (self.getSearch_SuningGray(),self.getList_SuningGray())
        else:
            return ""


# print(ConfigUtil().getRun('casePattern'))