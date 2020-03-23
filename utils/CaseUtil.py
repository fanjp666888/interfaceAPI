#! /usr/bin/python3
# -*- coding: utf8 -*-
import os
import unittest
from utils.Constant import Constant


class CaseUtil:
    def __init__(self):
        self.case_path = os.path.join(os.getcwd(), Constant.PATH_FOR_CASES)  # case路径：interfaceAPI/cases

    def filter(self, filterpattern):
        """过滤执行符合条件的脚本:unittest匹配"""
        testunit = unittest.TestSuite()
        discover = unittest.defaultTestLoader.discover(self.case_path, pattern=filterpattern)

        for test_suite in discover:
            for test_case in test_suite:
                testunit.addTest(test_case)

        return testunit
        # return discover



