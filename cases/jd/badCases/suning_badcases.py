#! /usr/bin/python3
# -*- coding: utf8 -*-
import logging, datetime, os

import unittest
from utils.LogSingleton import LogSingleton
from utils.Constant import Constant
from utils.ConfigUtil import ConfigUtil
from utils.KeywordUtil import KeywordUtil
from utils.ReportUtil_badcase import BabCase1_ReportUtil


logger = LogSingleton().getInstance()
logger = logging.getLogger(Constant.LOGGER_NAME)

class badCases(unittest.TestCase):
    CHECK_RANDOM_KEYWORD_NUM = 100
    searchresults = []
    writeExcelFlag = True
    @classmethod
    def setUpClass(self):
        logger.info("---start test suite(%s)---" % __name__)
        if self.writeExcelFlag:
            self.startTime = datetime.datetime.now()
            config = ConfigUtil()
            self.environment = config.getSelectedEnvironment()
            self.search = self.environment[0]
            self.list = self.environment[1]
            self.assertIsNot(self.environment, "", "Please choose one environment to run!")
            self.file_path = os.path.join(os.getcwd(), Constant.PATH_FOR_FILES)
            file_abspath = os.path.join(self.file_path, "topQuery_suning_1million.txt")
            self.ku = KeywordUtil(file_abspath)
    @classmethod
    def tearDownClass(self):
        if self.writeExcelFlag:
            self.stopTime = datetime.datetime.now()
            duration = str(self.stopTime - self.startTime)
            startTime = str(self.startTime)[:19]
            duration = duration[:duration.find(".")]
            ReportUtil1 = BabCase1_ReportUtil()
            ReportUtil1.generateReport(startTime, duration, self.searchresults)

        logger.info("---end test suite(%s)---" % __name__)

    def tmp_test_badCases1(self):
        pass
























