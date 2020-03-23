#! /usr/bin/python3
# -*- coding: utf8 -*-
import logging,urllib.parse,datetime,re,os
import unittest
from utils.ExcelUtil import ExcelUtil
from utils.LogSingleton import LogSingleton
from utils.Constant import Constant
from utils.SpiderUtil import SpiderUtil
from format.suning.SearchResult import SearchResult
from utils.ReportUtil_badcase4 import BabCase4_ReportUtil
from utils.KeywordUtil import KeywordUtil
from utils.ConfigUtil import ConfigUtil

logger = LogSingleton().getInstance()
logger = logging.getLogger(Constant.LOGGER_NAME)

class badCases(unittest.TestCase):
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
            file_abspath = os.path.join(self.file_path, "telephone.txt")
            self.ku = KeywordUtil(file_abspath)
    @classmethod
    def tearDownClass(self):
        if self.writeExcelFlag:
            self.stopTime = datetime.datetime.now()
            duration = str(self.stopTime - self.startTime)
            startTime = str(self.startTime)[:19]
            duration = duration[:duration.find(".")]
            if self.searchresults!=[]:
                ReportUtil4 = BabCase4_ReportUtil()
                ReportUtil4.generateReport(startTime, duration, self.searchresults)
        logger.info("---end test suite(%s)---" % __name__)

    def test_badCase4(self):
        """针对搜索手机搜索词，配件排在手机的前面的问题。
        从京东抓取不同品牌的手机类型作为query进行搜索"""
        self.flag = True
        #********方式一：通过excel表格的形式输入keyword*********************
        # excelPath = os.path.join(self.file_path, "xiaoMI.xlsx")
        # keywords = self.getKeyword(excelPath)[100:200]
        #********方式二：通过京东爬取的手机信息输入keyword********************
        keywords = self.ku.getAllKeywords()[151:161] #设置测试keyword个数
        #******单独测试*******
        # path = "C:\\Users\\jd\\PycharmProjects\\qa-search\\files\\telephone.txt"
        # self.ku = KeywordUtil(path)
        # keywords = self.ku.getAllKeywords()[90:150]
        # keywords = ["ZTEZ999"]
        for keyword in keywords:
            logger.info("测试query=%s"%keyword)
            flagList, checkResult = self.getShop(keyword)
            self.checkSort(keyword, flagList, checkResult)
        assert self.flag == True

    def getKeywordByExcel(self,excelPath):
        """通过excel表格方式输入搜索词"""
        excel = ExcelUtil()
        baseKey = excel.getColumnData(excelPath,"Sheet1",0)
        list1 = (excel.getColumnData(excelPath,"Sheet1",1))
        list1.insert(0,'')
        list2 = excel.getColumnData(excelPath, "Sheet1", 2)
        list2.insert(0, '')
        list3 = excel.getColumnData(excelPath, "Sheet1", 3)
        list3.insert(0, '')
        list4 = excel.getColumnData(excelPath, "Sheet1", 4)
        list4.insert(0, '')
        keywords = []
        for key in baseKey:
            for a in list1:
                Str = key
                Str += a
                for b in list2:
                    Strb = Str[:]
                    Strb += b
                    for c in list3:
                        Strc = Strb[:]
                        Strc += c
                        for d in list4:
                            Strd = Strc[:]
                            Strd += d
                            keywords.append(Strd)

        return keywords

    def isExistErrorKey(self,breadcrumb_title):
        """判断配件类的词是够命中title和breadcrumn_title"""
        errorKey = ["配件", "数据线", "手机壳", "保护壳", "贴膜", "保护套", "手写笔", "耳机", "充电线", "吸盘", "U盘","充电器"]
        breadcrumb_title = re.sub(r"(【.+】)|(（.+）|(送.+\*))|(\+.+)", "", breadcrumb_title)
        for key in errorKey:
            if key in breadcrumb_title:
                return False
        return True #没有包含配件这些词

    def isExistGoalKey(self,soup):
        """判断目标词“手机”是否命中分类"""
        threeGroup = soup.find_all('a', class_="ft")
        for group in threeGroup:
            if group.string == "手机"or group.string == "二手手机":
                return True
        return False

    def getShop(self,keyword):
        """取出前30个商品,并判断是否为配件"""
        goalKey = "手机"
        configutil = ConfigUtil()
        URL = configutil.getSearch_SuningPrd()+"/"+urllib.parse.quote(keyword)
        # URL = "http://search.suning.com"+"/"+urllib.parse.quote(keyword)
        response = SpiderUtil.getHtml(URL + "/")
        vonder_shops = re.findall(r'<li docType="1".*id="(.*?)"',response) + re.findall(r'<div.*product-box  basic.*id="(.*?)"',response)
        flagList = []
        checkResult = {}  # 报告中使用
        for vonder_shop in vonder_shops:
            goalFlag = 0
            number =vonder_shop.split("-")
            url = "https://product.suning.com/"+number[0]+"/"+number[1]+".html"
            soup = SpiderUtil.getSoupContent(url)
            logger.info("测试商品: %s"%vonder_shop)
            breadcrumb_title = ""
            if soup != "":
                breadcrumb_title_tmp = SpiderUtil.findContentbyTagClass(soup, "span", "breadcrumb-title")
                if breadcrumb_title_tmp!=[]:
                    breadcrumb_title = breadcrumb_title_tmp[0]["title"]
                if self.isExistErrorKey(breadcrumb_title):
                        if self.isExistGoalKey(soup):
                            goalFlag = 1 #表示此商品是手机
            flagList.append(goalFlag)
            if goalFlag == 1:
                checkResult.update({number[1]:goalKey})
            else:
                checkResult.update({number[1]:"配件"})
        return flagList,checkResult

    def checkSort(self,keyword,flagList,checkResult):
        """判断是否有配件排在了手机的前面"""
        label = 1
        for f in flagList:
            if f == 0:
                index = flagList.index(f)
                if index+1 < len(flagList):#防止未最后一位的情况
                    if 1 in flagList[index+1:]:
                        label = 0
        if 1 not in flagList:
            label=0
        # ************报告**************
        result = SearchResult()
        if label == 1:
            wordMatch = "pass"
        else:
            wordMatch = "fail"
            self.flag = False
        result.setKeyword(keyword)
        result.setCheckResult(checkResult)
        result.setMatchStatus(wordMatch)
        self.searchresults.append(result)



