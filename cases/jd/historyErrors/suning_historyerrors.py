#! /usr/bin/python3
# -*- coding: utf8 -*-
import logging
import unittest
from utils.LogSingleton import LogSingleton
from utils.Constant import Constant

logger = LogSingleton().getInstance()
logger = logging.getLogger(Constant.LOGGER_NAME)

class historyErrors(unittest.TestCase):
        
    @classmethod
    def setUpClass(self):
        logger.info("---start test suite(%s)---" % __name__)

    @classmethod
    def tearDownClass(self):
        logger.info("---end test suite(%s)---" % __name__)

    def test_historyErrors(self):
        """ 测试历史问题，确保不会再次出现"""
        pass