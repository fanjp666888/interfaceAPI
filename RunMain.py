#! /usr/bin/python3
# -*- coding: utf8 -*-
import logging
import os
import time
import unittest
# from utils import HTMLSearchReport
from utils import HTMLTestRunner as HTMLSearchReport
from utils.CaseUtil import CaseUtil
from utils.ConfigUtil import ConfigUtil
from utils.Constant import Constant
from utils.LogSingleton import LogSingleton

if __name__ == '__main__':
    config = ConfigUtil()
    # 选择去运行case目录下的哪些自动化脚本
    casePattern = config.getRun(Constant.CONFIG_PARAM_RUN_PATTERN)

    logger = LogSingleton()
    logger = logging.getLogger(Constant.LOGGER_NAME)
    
    # 报告存放路径
    report_path = os.path.join(os.getcwd(), Constant.PATH_FOR_REPORTS)
    
    now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    report_abspath = os.path.join(report_path, "report_" + now + ".html")
    fp = open(report_abspath, 'wb')
    logger.info("Created a report file(%s)" % report_abspath)
    runner = HTMLSearchReport.HTMLTestRunner(stream=fp,
                                           verbosity=2,
                                           title=Constant.REPORT_TITLE,
                                           description=Constant.REPORT_DESCRIPTION,
                                           )
    logger.info("========== Starting automation run ==========")
    runner.run(CaseUtil().filter(casePattern))
    fp.close()
    logger.info("========== Completed automation run ==========")


