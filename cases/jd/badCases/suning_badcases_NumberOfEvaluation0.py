#! /usr/bin/python3
# -*- coding: utf8 -*-

import urllib.request
import urllib.parse
import re
from json import JSONDecodeError
import requests
import json
import os
import logging
import unittest
import datetime
from utils.Constant import Constant
from utils.KeywordUtil import KeywordUtil
from utils.RequestUtil import RequestUtil
from utils.ConfigUtil import ConfigUtil
from utils.ExcelUtil import ExcelUtil
from format.suning.SearchResult import SearchResult

logger = logging.getLogger(Constant.LOGGER_NAME)
req = RequestUtil()
config = ConfigUtil()

"""评价数为0的商品排序靠前"""
class NumberOfEvaluation0(unittest.TestCase):
    all_results = []

    @classmethod
    def setUpClass(self):
        self.startTime = datetime.datetime.now()
        logger.info("---start test suite(%s)---" % __name__)
        file_path = os.path.join(os.getcwd(), Constant.PATH_FOR_FILES)
        file_abspath = os.path.join(file_path, "topQuery_suning_1million.txt")
        # topQuery_suning_1million.txt  topQuery.txt   test.txt
        self.all_keywords = KeywordUtil(file_abspath).getAllKeywords()

    @classmethod
    def tearDownClass(self):
        excel = ExcelUtil()
        excel.export_commodity_type_judgment_results_to_excel('NumberOfEvaluation0.xls', self.all_results)
        logger.info("---end test suite(%s)---" % __name__)

    def test_commodity_type_judgment(self):
        keywords = self.all_keywords
        for i in range(len(keywords)):
            result = SearchResult()
            test_result = ''
            set_result_detail = ''
            print(keywords[i])
            url = "https://search.suning.com/" + urllib.parse.quote(keywords[i]) + "/&query=true"
            #print(url)
            data_url = urllib.request.urlopen(url)
            data = str(data_url.read(), encoding='utf-8')
            with open('url.txt', 'w+', encoding='utf-8') as file:
                file.write(data)
            with open('url.txt', "r", encoding='utf-8') as file:
                redo = None
                http = None
                http_port = None
                for line in file:
                    http_tmp = re.search(r'http://searchapi.cnsuning.com:4008.+key', line)
                    if http_tmp != None:
                        http = http_tmp.group()
                        redo = re.search(r'redo=1', http)
                        if redo != None:
                            http_port = http[0:len(http) - 7]
                if redo == None and http != None:
                    http_port = http[0:len(http) - 7]
                elif http == None:
                    logger.info('此网页中没有找到接口URL')
            if http_port != None:
                query_check = re.search(r'q=' + keywords[i], http_port)
                query_Noresult = re.search(r'搜索结果页-无结果页面', data)
                if query_check != None:
                    http_port = re.sub(r'wt=protolbuf', 'wt=json&debug_info=as', http_port)
                    response = requests.get(http_port)
                    tem = response.text
                    try:
                        tem1 = json.loads(tem)
                        logger.info(keywords[i])
                        for y in range(50):
                            a = tem1['as']['as_response']['sub_query_response_list'][0]['results']['doc_list'][y]['countOfarticle']
                            b = tem1['as']['as_response']['sub_query_response_list'][0]['results']['doc_list'][y + 1]['countOfarticle']
                            c = tem1['as']['as_response']['sub_query_response_list'][0]['results']['doc_list'][y]['index']
                            d = tem1['as']['as_response']['sub_query_response_list'][0]['results']['doc_list'][y + 1]['countOfarticle']
                            if int(float(a)) == 0 and int(float(b)) > 0:
                                logger.info(keywords[y] + '第' + str(y) + '个出错了价格等于0')
                                test_result = 'fail'
                                set_result_detail = '中第%d个商品错误 ' % (y) + ":" + keywords[y]
                                if y >= 30:
                                    logger.info('break')
                                    break
                            else:
                                test_result = 'pass'
                                set_result_detail = "正确"
                    except JSONDecodeError:
                        test_result = 'Error'
                        logger.info(keywords[i] + ",json异常")
                        set_result_detail = '非常抱歉！json异常'
            result.setKeyword(keywords[i])
            result.set_result_detail(set_result_detail)
            result.set_test_result(test_result)
            self.all_results.append(result)
