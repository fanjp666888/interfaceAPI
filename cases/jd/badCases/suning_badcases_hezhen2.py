#! /usr/bin/python3
# -*- coding: utf8 -*-
import logging,urllib.parse,datetime,os
import unittest
from utils.LogSingleton import LogSingleton
from utils.Constant import Constant
from utils.ConfigUtil import ConfigUtil
from utils.RequestUtil import RequestUtil
from format.suning.SearchResult import SearchResult
from utils.KeywordUtil import KeywordUtil
from utils.ReportUtil_badcase2 import BabCase2_ReportUtil

logger = LogSingleton().getInstance()
logger = logging.getLogger(Constant.LOGGER_NAME)

class badCases(unittest.TestCase):
    CHECK_RANDOM_KEYWORD_NUM = 100
    searchresults2 = []
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
            if self.searchresults2!=[]:
                ReportUtil2 = BabCase2_ReportUtil()
                ReportUtil2.generateReport(startTime, duration, self.searchresults2)

        logger.info("---end test suite(%s)---" % __name__)

    def test_badCase2(self):
        """3.11：关键词：T恤，现结果页展示的全身体育的商品
          --》运动t桖分类得分高一点儿，修改了权重
          思路：1.原始文件（所有分类的集合），
	            2.取出关键命中的分类，分析分类是否在同一级或二级目录下，
                3.自定义分类，分析query命中的分类是否在自定义分类的同一级目录下-->目前没有想好怎么分类"""
        self.flag_keywords = []
        keywords = self.ku.getRandomKeywords(self.CHECK_RANDOM_KEYWORD_NUM)
        # keywords = ["格力（gree）3匹i尚一级能效变频冷暖智能wifi圆柱空调柜机（白色）kfr-72lw/(72555)fnhaa-a1"]
        for keyword in keywords:
            self.compare_level(keyword)
        assert 1 not in self.flag_keywords
    def compare_level(self,keword):
        self.oneLevel = [] #从文件中存储的一级、二级、三级目录id列表
        self.twoLevel = []
        self.thereLevel = []
        allLevelId = []
        HitLevels = self.get_HitLevel(keword)  # 命中的 {目录id：权重值} 组成的字典
        HitLevelsId = list(HitLevels.keys())  # 命中的目录id
        HitLevelsValue = list(HitLevels.values())
        readlines = self.catalog.getAllKeywords()
        self.get_InfoFromfile(readlines)  # 从文件中取出一级，二级，三级目录id列表
        IdList = list(map(self.getID,HitLevelsId))  # 命中目录在第几级目录1,2,3

        for i in range(len(IdList)):
            tmp = []
            if IdList[i] == 1:#若命中一级，存储[权重，一级目录id，0]
                tmp.extend([HitLevelsValue[i],HitLevelsId[i],"0"])
            elif IdList[i] == 2:#若命中二级，存储[权重，一级目录id，二级目录id]
                oneLevelId = self.oneLevel[self.twoLevel.index(HitLevelsId[i])]
                tmp.extend([HitLevelsValue[i],oneLevelId,HitLevelsId[i]])
            elif IdList[i] == 3:#若命中三级,存储[权重，一级目录id，二级目录id]
                oneLevelId = self.oneLevel[self.thereLevel.index(HitLevelsId[i])]
                twoLevelId = self.twoLevel[self.thereLevel.index(HitLevelsId[i])]
                tmp .extend([HitLevelsValue[i],oneLevelId,twoLevelId])
            else:
                tmp.extend(["命中目录未在文件中找到"])
            allLevelId.append(tmp)  #将三个命中的目录以二维的形式存储[[目录名字1，目录id1，目录id2],[],[]]
        #************对比目录情况****************
        flag_keyword = 0
        wordMatch = "pass"
        if 4 not in IdList:
            for j in range(len(allLevelId)-1):
                if self.compare_TwoHitLevel(allLevelId[j],allLevelId[j+1]):
                    flag_keyword = 1
                    wordMatch = "fail"
            if len(IdList) == 3:
                if self.compare_TwoHitLevel(allLevelId[0],allLevelId[2]):
                    flag_keyword = 1
                    wordMatch = "fail"
        else:
            flag_keyword = 2
            wordMatch = "warn"
        self.flag_keywords.append(flag_keyword)
        #*************报告**************
        result = SearchResult()
        result.setKeyword(keword)
        result.setHitLevels(HitLevels)
        result.setlevelsAnalyzed(allLevelId)
        result.setMatchStatus(wordMatch)
        self.searchresults2.append(result)
    def get_HitLevel(self,keyword):
        """从wwsy中获取目录id和权重值"""
        Config = ConfigUtil()
        wwsy = Config.getRun("wwsy_prd") + urllib.parse.quote(keyword)
        # wwsy = "http://10.104.242.58/qa?&gender=1&rewrite=1&gender=1&import=1&rett=1&shop=1&source=search&semantic=1&gbk=0&q="+urllib.parse.quote(keyword)
        request = RequestUtil()
        reponse = request.get(wwsy, {})
        HitLevel = {}
        if reponse["sort_res"] != None:
            entitys = reponse["sort_res"][0]["entitys"]
            if entitys !=None:
                for entity in entitys[:3]:#只取前三个
                    HitLevel.update({entity["entity_id"]:entity["entity_s"]})
        return HitLevel
    def get_InfoFromfile(self,readlines):
        """从目录表中分别得到一级、二级、三级目录列表"""
        TwoDimension = []
        for line in readlines:
            TwoDimension.append(line.split(","))
        for a, b, c, d, e, f, g in TwoDimension:
            self.oneLevel.append(a)
            self.twoLevel.append(c)
            self.thereLevel.append(e)
    def getID(self,id1):
        """判断命中目录是第几级目录"""
        if id1 in self.oneLevel:
            return 1
        elif id1 in self.twoLevel:
            return 2
        elif id1 in self.thereLevel:
            return 3
        else:
            return 4  # 所命中目录没有在文件中
    def compare_TwoHitLevel(self,list1,list2):
        """比较两个目录的是否在同一个一级目录下或者在同一个二级目录下"""
        flag = 0
        if list1[2]!=list2[2]:#若二级目录不相等
            if list1[1]!=list2[1]:#若一级目录不相等
                pass
            else:
                if float(list1[0])-float(list2[0])>0.3:
                    flag = 1  # 表示权重值差别太大
        else:
            if float(list1[0])-float(list2[0])>0.3:
                flag = 1
        return flag

