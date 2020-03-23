#! /usr/bin/python3
# -*- coding: utf8 -*-
import logging
import unittest
from utils.LogSingleton import LogSingleton
from utils.Constant import Constant

logger = LogSingleton().getInstance()
logger = logging.getLogger(Constant.LOGGER_NAME)

class categoryHit(unittest.TestCase):
        
    @classmethod
    def setUpClass(self):
        logger.info("---start test suite(%s)---" % __name__)

    @classmethod
    def tearDownClass(self):
        logger.info("---end test suite(%s)---" % __name__)

    def test_categoryHit(self):
        """ 测试是否命中分类，及分类的正确性"""
        pass