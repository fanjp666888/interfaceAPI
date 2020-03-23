#! /usr/bin/python3
# -*- coding: utf8 -*-

import urllib.request
import urllib.parse
import re
import requests
import json
import os
import logging
import unittest
import datetime
import random
import time
from utils.Constant import Constant
from utils.KeywordUtil import KeywordUtil
from utils.RequestUtil import RequestUtil
from utils.ConfigUtil import ConfigUtil
from utils.ReportUtil_sort import ReportUtil_sort
from utils.ExcelUtil import ExcelUtil
from format.suning.SearchResult import SearchResult

logger = logging.getLogger(Constant.LOGGER_NAME)
req = RequestUtil()
config = ConfigUtil()

"""搜索＂德芙可可巧克力＂，搜索结果商品类型不正确"""
class CommodityTypeJudgment(unittest.TestCase):
    all_judgment_results = []

    @classmethod
    def setUpClass(self):
        self.startTime = datetime.datetime.now()
        logger.info("---start test suite(%s)---" % __name__)
        file_path = os.path.join(os.getcwd(), Constant.PATH_FOR_FILES)
        file_abspath = os.path.join(file_path, "commodityKeyword.txt")
        # topQuery_suning_1million.txt  topQuery.txt   test.txt
        self.all_keywords = KeywordUtil(file_abspath).getAllKeywords()

    @classmethod
    def tearDownClass(self):
        excel = ExcelUtil()
        excel.export_commodity_type_judgment_results_to_excel('commodity_type_judgment_result.xls', self.all_judgment_results)
        logger.info("---end test suite(%s)---" % __name__)

    def test_commodity_type_judgment(self):
        keywords = self.all_keywords
        for keyword_info in keywords:
            result = SearchResult()
            test_result = ''
            set_judgment_result_detail = ''
            keyword = keyword_info.split(',')[0]
            keyword_type = keyword_info.split(',')[1]
            url = "http://search.suning.com/" + urllib.parse.quote(keyword) + "/&query=true"
            data_url = urllib.request.urlopen(url)
            data = str(data_url.read(), encoding='utf-8')
            with open('url.txt', 'w+', encoding='utf-8') as file:
                file.write(data)
            with open('url.txt', "r", encoding='utf-8') as file:
                redo = None
                http = None
                http_port = None
                for line in file:
                    http_tmp = re.search(r'http://searchapi.cnsuning.com.+key', line)
                    if http_tmp != None:
                        http = http_tmp.group()
                        redo = re.search(r'redo=1', http)
                        if redo != None:
                            http_port = http[0:len(http) - 7]
                if redo == None and http != None:
                    http_port = http[0:len(http) - 7]
                elif http == None:
                    logger.info('此网页中没有找到接口URL')
            if http_port is not None:
                query_no_result = re.search(r'搜索结果页-无结果页面', data)
                if query_no_result is not None:
                    test_result = 'fail'
                    set_judgment_result_detail = '非常抱歉！没有找到与' + keyword + '相关的商品'
                else:
                    http_port = re.sub(r'wt=protolbuf', 'wt=json&debug_info=as', http_port)
                    all_result = requests.get(http_port)
                    commodity_info = json.loads(all_result.text.replace('\\"', '').replace('\\', ''))
                    commodity_num = len(
                        commodity_info['as']['as_response']['sub_query_response_list'][0]['results']['doc_list'])
                    if commodity_num > 10:
                        num = 10
                    else:
                        num = commodity_num
                    flag = 0
                    for i in range(num):
                        commodity_type = \
                            commodity_info['as']['as_response']['sub_query_response_list'][0]['results']['doc_list'][i][
                                'three_groupName']
                        if keyword_type not in commodity_type:
                            flag += 1
                            set_judgment_result_detail = set_judgment_result_detail + '第%d个商品类型错误 ' % (i+1)
                    if flag != 0:
                        logger.info(keyword + "有问题")
                        test_result = 'fail'
                    else:
                        logger.info(keyword + "没问题")
                        test_result = 'pass'
            result.set_result_detail(set_judgment_result_detail)
            result.setKeyword(keyword)
            result.set_test_result(test_result)
            self.all_judgment_results.append(result)

