#! /usr/bin/python3
# -*- coding: utf8 -*-
import datetime
import json
import logging
import os
import sys
import time
import unittest
import urllib
import requests
from utils.ConfigUtil import ConfigUtil
from utils.Constant import Constant
from utils.FileUtil import FileUtil
from utils.LogSingleton import LogSingleton
from utils.SegmentUtil import SegmentUtil
from utils.SpiderUtil import SpiderUtil

logger = LogSingleton().getInstance()
logger = logging.getLogger(Constant.LOGGER_NAME)

class brandHit(unittest.TestCase):
    
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
        brand_path = os.path.join(file_path, "brand_total.txt")
        keyword_path = os.path.join(file_path, "topQuery.txt")
        
        self.brandlist = FileUtil(brand_path).getAllLines()
        self.keywords = FileUtil(keyword_path).getAllLines()
        self.wwsyURL = config.getRun(Constant.CONFIG_PARAM_RUN_WWSY)  

    @classmethod
    def tearDownClass(self):
        logger.info("---end test suite(%s)---" % __name__)

    def test_brandHit(self):
        """ 测试是否命中品牌"""
        #keywords = ["开能净水器","美的小冰箱","iPhoneX","华为手机","小米手机","vivo手机"]
        #keywords = ["iPhoneX"]
        keywords = self.keywords
        self.checkBrandHit(keywords)
        
    def checkBrandHit(self,keywords):
        for keyword,num in zip(keywords,range(len(keywords))):
            logger.info("=============keyword(%s) = %s" % (1+num,keyword))
            url = self.search+"/"+urllib.parse.quote(keyword)+"/"
            soup = SpiderUtil.getSoupContent(url)
            brand = SpiderUtil.getBrand(soup)
            if brand == "未命中":
                brand = ""
            brand_wwsy = self.getBrandFromWWSY(keyword)
            if brand_wwsy == "":
                brand_wwsy = keyword
            brand_wwsy_array = brand_wwsy.split("(")
            logger.info("wwsy brand = %s" % brand_wwsy)
            self.verifyBrandHitConditions(brand_wwsy_array,brand,self.brandlist)
            
    def verifyBrandHitConditions(self,brand_wwsy_array,brand,brandlist):
        findBrand = False
        brandarray = brand.split("(")
        for brand_wwsy in brand_wwsy_array:
            brand_wwsy = brand_wwsy.replace(")","")
            #logger.info("verifyBrandHit: wwsy brand = %s" % brand_wwsy)
            if self.findBrandInTotalBrandlist(brand_wwsy, brandlist) and brandarray[0] in brand_wwsy:
                logger.info("=======Hit brand = %s" % brand)
                findBrand = True
                break
        if not findBrand:
            sys.stderr.write("\nError: Not hit brand = %s, wwsy brand = %s" % (brand,brand_wwsy))
    
    def findBrandInTotalBrandlist(self,keyword,brandlist):
        brandlist_lower = [item.lower() for item in brandlist]
        words = SegmentUtil().getSuningWordSegments(keyword)
        for word in words:
            if word.lower() in brandlist_lower:
                logger.info("*** Found keyword(%s) in brandlist ***" % keyword)
                return True
        return False
     
    def getBrandFromWWSY(self,data):
        try_times = 3
        try_num = 0
        brand = ""
        while try_num<try_times:
            try_num += 1
            #logger.info("Try(%s)" %try_num)
            response = requests.get(self.wwsyURL+data)
            result = json.loads(response.text)
            if result['sort_res'] != None and result['sort_res'][1]['entitys'] != None:
                #groupId = result['sort_res'][0]['entitys'][0]['entity_id']
                brand = result['sort_res'][1]['entitys'][0]['entity_v']  
                #logger.info("group id = %s, brand = %s" % (groupId,brand)) 
                break
            time.sleep(1)
        return brand