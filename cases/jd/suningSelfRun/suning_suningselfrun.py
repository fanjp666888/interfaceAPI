#! /usr/bin/python3
# -*- coding: utf8 -*-
import datetime
import logging
import os
import re
import threading
import unittest
import urllib
from utils.ConfigUtil import ConfigUtil
from utils.Constant import Constant
from utils.KeywordUtil import KeywordUtil
from utils.LogSingleton import LogSingleton
from utils.SpiderUtil import SpiderUtil

logger = LogSingleton().getInstance()
logger = logging.getLogger(Constant.LOGGER_NAME)

class suningSelfRun(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        logger.info("---start test suite(%s)---" % __name__)
        self.startTime = datetime.datetime.now()
        config = ConfigUtil()
        self.environment = config.getSelectedEnvironment()
        self.search = self.environment[0]
        self.list = self.environment[1]
        
        self.assertIsNot(self.environment,"","Please choose one environment to run!")
        
        file_path = os.path.join(os.getcwd(), Constant.PATH_FOR_FILES)
        file_abspath = os.path.join(file_path, "topQuery.txt")
        self.ku = KeywordUtil(file_abspath)
        
        self.error_list = []

    @classmethod
    def tearDownClass(self):
        logger.info("---end test suite(%s)---" % __name__)
    
    def singlethread_suningSelfRun(self):
        """ 测试勾选苏宁自营，是否有非苏宁自营的商品展示出来"""
        #keywords = ["洗衣机","美的小冰箱","冰箱","手机","空气净化器","iPhoneX","良品铺子","三只松鼠","电磁炉","华为mate20","华为手机"]
        keywords = self.ku.getAllKeywords()
        #keywords = ["华为手机"]
        selfrun_urls = self.getSuningSelfRunURL(keywords)
        errors = self.findSelfRunIssues(selfrun_urls,keywords)
        num = 0
        for error in errors:
            num += 1
            print("Issues for jd self runs (%d) = %s" % (num,error))
    
    def test_suningSelfRun(self):
        global lock
        lock=threading.Lock()
        threads = []
        totalThread = 5
        len_total = len(self.ku.getAllKeywords())
        gap = int(len_total / totalThread) 
        for i in range(totalThread):
            thread = 'thread%s' % i
            if i == 0:
                thread = threading.Thread(target=self.checkSelfrun,args=(self.ku.getKeywords(0, gap),))
            elif totalThread==i+1:
                thread = threading.Thread(target=self.checkSelfrun,args=(self.ku.getKeywords(i*gap, len_total),))
            else:
                thread = threading.Thread(target=self.checkSelfrun,args=(self.ku.getKeywords(i*gap, (i+1)*gap),))
            threads.append(thread) 
        # 循环开启线程
        for i in range(totalThread):
            threads[i].start()
        # 等待所有线程完成
        for t in threads:
            t.join()
        logger.info("Completed, found %d errors." %len(self.error_list))
         
    def checkSelfrun(self,keywords):
        selfrun_urls = self.getSuningSelfRunURL(keywords)
        errors = self.findSelfRunIssues(selfrun_urls,keywords)
        lock.acquire()
        self.error_list += errors
        lock.release()
        
    def getSuningSelfRunURL(self,keywords):
        urls = []
        for keyword,num in zip(keywords,range(len(keywords))):
            logger.info(("keyword(%s) = %s" % (1+num,keyword)))
            url = self.search+"/"+urllib.parse.quote(keyword)+"/"
            soup = SpiderUtil.getSoupContent(url)
            if soup == "":
                continue
            brand = SpiderUtil.getBrand(soup)
            
            #check whether have suggest keyword
            if len(soup.find_all("strong"))>2:
                suggest_message = soup.find_all("strong")[0].text
                suggest_keyword = suggest_message.split("\"")[1]
                url = self.search+"/"+urllib.parse.quote(suggest_keyword)+"/"
                
            suningSelfRun_URL = url + "&isNoResult=0"
            
            #check whether have ci number
            try:
                categoryId = soup.find("script").text.split("\"categoryId\":")[1].split(",")[0]
            except AttributeError:
                continue
            category = int(re.sub("\D","",categoryId))
            if category != 0:
                suningSelfRun_URL += "&ci="+str(category)
            
            #check whether have brand selected    
            if brand!="未命中":
                brand = urllib.parse.quote(brand).replace("%E3%80%81", "%3B")
                suningSelfRun_URL += "&hf=brand_Name_FacetAll:"+brand
            #logger.info("Hit brand = %s" % brand)
            
            suningSelfRun_URL += "&sc=0&ct=1&snyp=&st=0#second-filter"
 
            #logger.info("suningSelfRun_URL = %s" % suningSelfRun_URL)
            #logger.info("==============================")
            urls.append(suningSelfRun_URL)
        return urls
    
    def findSelfRunIssues(self,selfrun_urls,keywords):
        error_list = []
        num = 0
        for url in selfrun_urls:
            soup = SpiderUtil.getSoupContent(url)
            num_product = self.getProductNum(soup)
            num_selfrun = self.getSelfrunNum(soup)
            if num_product != num_selfrun:
                error_list.append(keywords[num])  
            num += 1  
        return error_list 
            
    def getProductNum(self,soup):
        num_product = soup.find_all('div', class_='img-block')
        return len(num_product)
    
    def getSelfrunNum(self,soup):
        num_selfrun = soup.find_all('div', class_='store-stock')
        return len(num_selfrun)