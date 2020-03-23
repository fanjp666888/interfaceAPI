#! /usr/bin/python3
# -*- coding: utf8 -*-


class SearchResult:
    
    def __init__(self):
        self.keyword = ""
        self.words = []
        self.brand = ""
        self.category = ""
        self.totalcount = 0
        self.pagenum = 0
        self.matchstatus = None
        self.distance = 0
        self.unmatched = []
        self.sort_result = ""
        self.sort_result_detail = ""
        self.sort_type = ""
        self.test_result = ""
        self.result_detail = ""
        self.hitLevels = {}
        self.levelsAnalyzed = []
        self.title = []
        self.hitrate = []
        self.averagehitrate = []
        self.checkResult ={}

    def getKeyword(self):
        return self.keyword
    def getWords(self):
        return self.words
    def getBrand(self):
        return self.brand
    def getCategory(self):
        return self.category
    def getTotalCount(self):
        return self.totalcount
    def getPageNum(self):
        return self.pagenum
    def getMatchStatus(self):
        return self.matchstatus
    def getDistance(self):
        return self.distance
    def getUnmatched(self):
        return self.unmatched

    def get_sort_result(self):
        return self.sort_result

    def get_sort_result_detail(self):
        return self.sort_result_detail

    def get_sort_type(self):
        return self.sort_type

    def get_test_result(self):
        return self.test_result

    def get_result_detail(self):
        return self.result_detail

    def getBrand_wwsy(self):
        return self.brand_wwsy

    def getHitLevels(self):
        return self.hitLevels

    def getlevelsAnalyzed(self):
        return self.levelsAnalyzed

    def getTitle(self):
        return self.title

    def getHitRate(self):
        return self.hitrate

    def getAverageHitRate(self):
        return self.averagehitrate
    def getCheckResult(self):
        return self.checkResult

    def setKeyword(self,q):
        self.keyword = q
    def setWords(self,words):
        self.words = words
    def setBrand(self,brand):
        self.brand = brand 
    def setCategory(self,category):
        self.category = category 
    def setTotalCount(self,totalcount):
        self.totalcount = totalcount 
    def setPageNum(self,pagenum):
        self.pagenum = pagenum
    def setMatchStatus(self,matchstatus):
        self.matchstatus = matchstatus 
    def setDistance(self,distance):
        self.distance = distance
    def setUnmatched(self,unmatched):
        self.unmatched = unmatched

    def set_sort_result(self, sort_result):
        self.sort_result = sort_result

    def set_sort_result_detail(self, sort_result_detail):
        self.sort_result_detail = sort_result_detail

    def set_sort_type(self, sort_type):
        self.sort_type = sort_type

    def set_test_result(self, test_result):
        self.test_result = test_result

    def set_result_detail(self, result_detail):
        self.result_detail = result_detail

    def setBrand_wwsy(self, brand_wwsy):
        self.brand_wwsy = brand_wwsy

    def setHitLevels(self, hitLevels):
        self.hitLevels = hitLevels

    def setlevelsAnalyzed(self, levelsAnalyzed):
        self.levelsAnalyzed = levelsAnalyzed

    def setTitle(self, title):
        self.title = title

    def setHitRate(self, hitrate):
        self.hitrate = hitrate

    def setAverageHitRate(self, averagehitrate):
        self.averagehitrate = averagehitrate
    def setCheckResult(self,checkResult):
        self.checkResult = checkResult
if __name__ == '__main__':
    pass
