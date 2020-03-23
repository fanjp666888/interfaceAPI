#! /usr/bin/python3
# -*- coding: utf8 -*-
import datetime
import logging
import os
import time
import unittest
import urllib
from format.suning.SearchResult import SearchResult
from utils.ConfigUtil import ConfigUtil
from utils.SpiderUtil import SpiderUtil
from utils.ExcelUtil import ExcelUtil
from utils.KeywordUtil import KeywordUtil
from utils.LogSingleton import LogSingleton
from utils.ReportUtil import ReportUtil
from utils.SegmentUtil import SegmentUtil
from utils.Constant import Constant
from utils.RequestUtil import RequestUtil
logger = LogSingleton().getInstance()
logger = logging.getLogger(Constant.LOGGER_NAME)


class defaultDemo(unittest.TestCase):
    CHECK_RESULT_NUM = 5
    CHECK_RANDOM_KEYWORD_NUM = 1
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
            
            self.assertIsNot(self.environment,"","Please choose one environment to run!")
            
            file_path = os.path.join(os.getcwd(), Constant.PATH_FOR_FILES)
            file_abspath = os.path.join(file_path, "topQuery.txt")
            self.ku = KeywordUtil(file_abspath)
        
    @classmethod
    def tearDownClass(self):
        if self.writeExcelFlag:
            self.stopTime = datetime.datetime.now()
            duration = str(self.stopTime - self.startTime)
            startTime = str(self.startTime)[:19]
            duration = duration[:duration.find(".")]
            reportUtil = ReportUtil()
            reportUtil.generateReport(startTime,duration,self.searchresults)
            
            excel = ExcelUtil()
            excel.exportToExcel(startTime.replace(" ", "_").replace(":", "-", 2),self.searchresults)
        
        logger.info("---end test suite(%s)---" % __name__)

    # @unittest.skip('临时跳过test_add_enent_all_null')
    def test_add_enent_all_null(self, ):
        payload = '广西南宁瑞专商贸有限公司'
        self.base_url = "wwww.baidu.com"
        r = RequestUtil.request_main("get", self.base_url.format(payload))
        self.result = r.json()
        self.assertEqual(self.result['code'], 200)
        self.assertEqual(self.result['message'], 'success')

    def test_titlesFromRandom(self):
        """ 验证titles from random search"""
        kewords_random = self.ku.getRandomKeywords(self.CHECK_RANDOM_KEYWORD_NUM)
        self.verifyResultbyKeyword(kewords_random)
           
    def check_titlesFromTop01To10(self):
        """ 验证titles from top 1 to 10 search"""
        keywords = self.ku.getKeywords(0, 10)
        self.verifyResultbyKeyword(keywords)
    
    def check_titlesFromTop11To20(self):
        """ 验证titles from top 11 to 20 search"""
        keywords = self.ku.getKeywords(10, 20)
        self.verifyResultbyKeyword(keywords)
    
    def check_titlesFromTop21To30(self):
        """ 验证titles from top 21 to 30 search"""
        keywords = self.ku.getKeywords(20, 30)
        self.verifyResultbyKeyword(keywords)   
    
    def test_default(self):
        pass   
      
    def check_test(self):
        keywords = ["ipad",]
        #keyword = "阿迪达斯双肩包"
        #keyword = "华为手机"
        #keyword = "洁柔抽纸小规格"
        #keyword = "10548054358"
        self.verifyResultbyKeyword(keywords)
         
    def verifyResultbyKeyword(self,keywords):
        num = 0
        for keyword in keywords:
            result = SearchResult()
            num += 1
            url = "http://search.suning.com/"+urllib.parse.quote(keyword)+"/"
            logger.debug("Be about to getSoupContent")
            soup = SpiderUtil.getSoupContent(url)
            
            logger.debug("Be about to getBrand")
            brand = SpiderUtil.getBrand(soup)
            logger.debug("搜索关键词(%d) = %s" % (num,keyword))
            
            logger.debug("品牌 = %s" % brand)
            
            words = self.getWordSegments(keyword)
            logger.debug("分词结果：("+",".join(words)+")")
                        
            titles = SpiderUtil.getTitles(soup, self.CHECK_RESULT_NUM)
            if len(titles)==0:
                logger.debug("Sorry,搜索无结果！")
            else:
                logger.debug("搜索召回结果(排名从前到后)：")
                title_id = 0
                match_all = 0
                match_part = 0
                match_none = 0
                for title in titles:
                    time.sleep(1)
                    title_id += 1
                    status = self.verifyWordSegments(words, title)
                    if status == True:
                        match_all += 1
                    else:
                        match_none += 1
                if match_all == self.CHECK_RESULT_NUM:
                    wordMatch = "pass"
                elif match_none == self.CHECK_RESULT_NUM:
                    wordMatch = "fail"
                else:
                    wordMatch = "warn"
            result.setKeyword(keyword)
            result.setBrand(brand)
            result.setWords(words)
            result.setCategory(SpiderUtil.getCategory(soup))
            result.setTotalCount(format(int(SpiderUtil.getTotalCount(soup)),","))
            result.setPageNum(SpiderUtil.getPageNum(soup))
            result.setMatchStatus(wordMatch)
            logger.debug("============================")
            self.searchresults.append(result)
    
    #返回分词后的结果列表
    def getWordSegments(self,keyword):
        #keyword = "美的小冰箱"
        data = "q=%s&call_type=ST_PROB" % keyword
        su = SegmentUtil()
        words = su.getWordSegments(data) 
        return words   
    
    #判断标题是否含有任何一个分词结果
    def verifyWordSegments(self,words,title):
        for word in words:
            if word.lower() in title.lower():
                return True
        return False