#! /usr/bin/python3
# -*- coding: utf8 -*-
import os
import yaml
import logging.config
from utils.Constant import Constant


class LogSingleton:
    def __init__(self, default_path=Constant.LOG_FILE_NAME,default_level=logging.DEBUG):
        path = default_path 
        debug_level = default_level
        self.setup_logging(path,debug_level)
    '''
    Use singleton design pattern to avoid creating multiple same log classes to read conf file
    '''
    def __new__(self, *args, **kw):
        if not hasattr(self, 'instance'):
            self.instance = super(LogSingleton, self).__new__(self, *args, **kw)
        return self.instance
    
    def getInstance(self):
        if self.instance:
            return self.instance
        else:
            self.__init__(self)
            return self.instance
    
    def setup_logging(self,path,debug_level):
        '''
        Setup logging configuration
        '''
        if os.path.exists(path):
            try:
                with open(path,'r',encoding=Constant.CHAR_SET_FILE) as f:
                    config = yaml.load(f)
                    logging.config.dictConfig(config)
            except ValueError:
                os.mkdir("logs")
        else:
            logging.basicConfig(level=debug_level)
            print('[ERROR] The input path (',path,') does not exist!')



