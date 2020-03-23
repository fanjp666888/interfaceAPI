#! /usr/bin/python3
# -*- coding: utf8 -*-
import logging
import unittest
from utils.LogSingleton import LogSingleton
from utils.Constant import Constant

logger = LogSingleton().getInstance()
logger = logging.getLogger(Constant.LOGGER_NAME)

class newQuery(unittest.TestCase):
        
    @classmethod
    def setUpClass(self):
        logger.info("---start test suite(%s)---" % __name__)

    @classmethod
    def tearDownClass(self):
        logger.info("---end test suite(%s)---" % __name__)

    def test_newQuery(self):
        """ 通过实时增量，测试新上架的商品是否可以搜索到"""
        pass