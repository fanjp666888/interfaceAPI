#! /usr/bin/python3
# -*- coding: utf8 -*-
import logging,urllib.parse,datetime,os,re
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import unittest
from utils.LogSingleton import LogSingleton
from utils.Constant import Constant
from utils.SpiderUtil import SpiderUtil
from utils.ConfigUtil import ConfigUtil
from utils.RequestUtil import RequestUtil
from format.suning.SearchResult import SearchResult
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
            self.catalog = KeywordUtil(os.path.join(self.file_path, "catalog.txt"))
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

    def test_badCases1(self):
        """badcase: 搜索潘婷小瓶，改写先推了小瓶，做了干预，
        ---》改写错误，修改了改写，小瓶是识别为物品了，物品比品牌权重高一些;
        改写之后：没有找到“潘婷小瓶”的相关商品,我们为您提供"潘婷"的搜索结果;
        思路：wwsy中得到命中品牌，页面中得到品牌信息，对比两处的品牌信息"""
        kewords_random = self.ku.getRandomKeywords(self.CHECK_RANDOM_KEYWORD_NUM)
        flag = self.compare_brand(kewords_random)
        assert flag

    def compare_brand(self,kewords_random):
        flag = True
        # kewords_random = ["http://t.cn/rs719hp"]
        for keyword in kewords_random:
            logger.info("测试keyword为：%s" % (keyword))
            brands = self.get_brand(keyword)
            logger.info("页面取得品牌：%s" % brands)
            Config = ConfigUtil()
            wwsy = Config.getRun("wwsy_prd") + urllib.parse.quote(keyword)
            logger.info(wwsy)
            request = RequestUtil()
            reponse = request.get(wwsy, {})
            # 空列表循环是否报错
            brand_wwsy = "未命中"
            # logger.info("问题%s"%tmp)
            if reponse["sort_res"]!=None:
                for member in reponse["sort_res"]:
                    tmp1 = member["entitys"]
                    if member["entitys"] != None:
                        for entitys in member["entitys"]:
                            if entitys["entity_n"] == "brand_Name":
                                brand_wwsy = entitys["entity_v"]  # 同时命中两个品牌的情况？？
                                break
                logger.info("wwsy取的品牌：%s" % brand_wwsy)
            if brand_wwsy in brands:
                wordMatch = "pass"
            else:
                if brand_wwsy == "未命中":
                    wordMatch = "pass"
                else:
                    wordMatch = "fail"
            if wordMatch == "fail":
                flag = False
            result = SearchResult()
            result.setBrand(brands)
            result.setBrand_wwsy(brand_wwsy)
            result.setKeyword(keyword)
            result.setMatchStatus(wordMatch)
            self.searchresults.append(result)
        return flag
    def get_brand(self,keyword):
        url = "http://search.suning.com/" + urllib.parse.quote(keyword) + "/"
        soup = SpiderUtil.getSoupContent(url)
        # logger.info("soup%s"%soup)
        brands = []
        if soup!="":
            # logger.info("soup%s"%soup)
            brands = SpiderUtil.getBrand(soup).split("、")  # 品牌点击数较少，没有发到阀值,品牌信息是不此处显示的
            if brands == ["未命中"]:
                li = soup.find_all("li",class_=re.compile("s-brand*"))#所以可能会显示在高筛区
                # logger.info("li:%s"%li)
                if li!=[]:
                    brands = []
                    for L in li:
                        brand = L.a.span.text
                        brands.append(brand)
        else:
            browser = webdriver.Chrome(executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
            browser.get(url)
            if self.isExist(browser, "goods-list"):
                brands.append(browser.find_element_by_class_name("goods-list")["title"])
            else:
                if self.isExist(browser, "brands"):
                    ul = browser.find_element_by_class_name("brands")
                    li = ul.find_elements_by_tag_name("li")
                    for L in li:
                        brands.append(L.get_attribute("title"))  # 可用xpath优化
                else:
                    brands.append("未命中")
            logger.info("品牌%s" % brands)
            browser.quit()
        return brands
    def isExist(self,browser,classname):
        flag = True
        try:
            browser.find_element_by_class_name(classname)
        except NoSuchElementException as e:
            flag = False
        return flag

