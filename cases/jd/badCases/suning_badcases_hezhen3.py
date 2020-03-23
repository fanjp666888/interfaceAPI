#! /usr/bin/python3
# -*- coding: utf8 -*-
import logging,urllib.parse,datetime,os,re
import unittest
from utils.LogSingleton import LogSingleton
from utils.Constant import Constant
from utils.SpiderUtil import SpiderUtil
from utils.ConfigUtil import ConfigUtil
from format.suning.SearchResult import SearchResult
from utils.KeywordUtil import KeywordUtil
from utils.ReportUtil_badcase3 import BabCase3_ReportUtil

logger = LogSingleton().getInstance()
logger = logging.getLogger(Constant.LOGGER_NAME)

class badCases(unittest.TestCase):
    CHECK_RANDOM_KEYWORD_NUM = 100
    searchresults3 = []
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
            if self.searchresults3!=[]:
                ReportUtil3 = BabCase3_ReportUtil()
                ReportUtil3.generateReport(startTime, duration, self.searchresults3)

        logger.info("---end test suite(%s)---" % __name__)
    def test_badCase3(self):
        """badcase:搜索“宠物电器”，出来的都是洗衣机，搜索“套装刀，结果都没有刀具
          通过计算关键词命中“标题”，“卖点”命中率，来衡量召回结果是否符合预期。
        """
        sny_file = os.path.join(self.file_path, "syn_brand.txt")
        syn_segs = KeywordUtil(sny_file)
        self.allLine = syn_segs.getAllKeywords()
        keywords = self.ku.getRandomKeywords(self.CHECK_RANDOM_KEYWORD_NUM)
        # keywords = ["小米手环nfc款"]
        flag,errorKey = self.verify_PrecisionRate(keywords)
        if errorKey!=[]:
            print("测试失败的query：%s"%errorKey)
        assert flag == 0
    def get_Syn(self,seg):
        """get分词的同义词"""
        first_row = []
        seconde_row = []
        syns = [seg]  # 同义词列表包括本身
        for line in self.allLine:
            new_line = line.strip().split("\t")
            first_row.append(new_line[0])
            seconde_row.append(new_line[1])
        syns.extend([seconde_row[i] for i in range(len(first_row)) if first_row[i] == seg])
        syns.extend([first_row[i] for i in range(len(seconde_row)) if seconde_row[i] == seg])
        return list(set(syns))
    def get_Seg(self,Str,word):
        """得到分词"""
        segs = []
        url ="http://search.suning.com/emall/search.do?debug_token=47005f2ee0c32840dd547a2d6f08998f&redo=0&sesab=BBBABBAB&debug_id=123456&keyword="
        reponse = SpiderUtil.getHtml(url+urllib.parse.quote(word))
        if Str == "index":
            seg = re.findall(r'"index_seg":"(.*?)"', reponse)
        elif Str == "query":
            seg = re.findall(r'"query_seg":"(.*?)"', reponse)
        if seg!=[]:
            segs = seg[0].split("|")
        return segs
    def deal_QuerySeg(self, keyword):
        """对keyword进行分词，找到同义词"""
        qurey_segList = []
        query_segs = self.get_Seg("query", keyword)
        redundancy_seg = ["官方", "旗舰", "店", "苏宁", "自营"]
        for i in redundancy_seg:
            if i in query_segs:
                query_segs.remove(i)
        for query_seg in query_segs:
            qurey_segList.append(self.get_Syn(query_seg))
        return qurey_segList
    def count_HitRat(self,syns_list,title):
        """qurey的分词以及分词的同义词是否命中搜索到的商品的"""
        count = 0
        for syns in syns_list:
            for syn in syns:
                syn_lower = syn.lower()
                if syn_lower in title.lower():
                    # 考虑英文大小写的问题  2.考虑简体字繁体字？？？3.单位词替换
                    # 4.考虑命中品牌，品牌的中文和英文的转换 5.数字变汉字
                    count += 1
                    break
                else:
                    # 数字转换
                    list_CH = ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十"]
                    list_arab = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", ]
                    intersection_arab = list(set(list(syn)) & set(list_arab))
                    intersection_CH = list(set(list(syn)) & set(list_CH))
                    if len(intersection_arab) != 0:
                        for i in intersection_arab:
                            syn_lower = syn_lower.replace(i, list_CH[list_arab.index(i)])
                        if syn_lower in title.lower():
                            count += 1
                            break
                    if len(intersection_CH) != 0:
                        for i in intersection_CH:
                            syn_lower = syn_lower.replace(i, list_arab[list_CH.index(i)])
                        if syn_lower in title.lower():
                            count += 1
                            break
        rate = float("%.2f"%float(count/len(syns_list)))  # 保留浮点数的小数点后两位
        return rate
    def check_HitBjOtherTxt(self,vonder_shop):
        """对于没有命中标题和卖点时，有可能命中通子码信息，
          本函数目的获取商品的通子码信息"""
        BjOtherTxt = []
        vonder_shop_Id = vonder_shop.split("-")
        url = "http://product.suning.com/"+vonder_shop_Id[0]+"/"+vonder_shop_Id[1]+".html"
        logger.info(url)
        soup = SpiderUtil.getSoupContent(url)
        for li in soup.find_all("li",class_="clr-item"):
            BjOtherTxt.append(li["title"])
        return BjOtherTxt
    def get_partnumber(self,url,keyword):
        """得到商品编码"""
        response = SpiderUtil.getHtml(url + "/" + urllib.parse.quote(keyword) + "/")
        ID = re.findall(r'<li docType="1".*id="(.*?)"',response) + re.findall(r'<div.*product-box  basic.*id="(.*?)"',response)
        return ID
    def verify_PrecisionRate(self,keywords):
        count = 0
        errorKey = []
        for keyword in keywords:
            logger.info("测试分词：%s"%keyword)
            keyword = keyword.replace("-", '%252d')  #quote对‘-’不编码
            RateSum = []
            result = SearchResult()
            config = ConfigUtil()
            url = config.getSearch_SuningPrd()
            soup = SpiderUtil.getSoupContent(url+"/"+urllib.parse.quote(keyword)+"/")
            vonder_shops = self.get_partnumber(url,keyword)
            logger.info(url+"/"+urllib.parse.quote(keyword)+"/")
            #**********处理qurey分词********************
            if soup != '':
                div = soup.find("div", class_="no-result-tips")  # 考虑推荐的情况，会有两个class[no-result-tips no-result-proposal]
                if div != None:
                    if len(div["class"]) == 1:  # 考虑改写的情况，用改写之后的值匹配
                        tmp = div.strong.text
                        keyword = re.findall(r'我们为您提供"(.*?)".*的搜索结果',div.strong.text)[0]
                qurey_segList = self.deal_QuerySeg(keyword)  # 存放query的每个分词找到同义词
                allShopNum = int(SpiderUtil.getTotalCount(soup))  # 考虑召回商品少于5个情况，没有召回商品的情况
                if allShopNum != 0:
                    if allShopNum > 4:
                        getShopNum = 5  # 取召回商品的前5个
                    else:
                        getShopNum = allShopNum
                    titles = SpiderUtil.getTitles(soup, getShopNum)
                    auxdescriptions = SpiderUtil.getAuxdescription(soup, getShopNum)
                    storenames = SpiderUtil.getStoreName(soup, getShopNum)
                    for k in range(len(titles)):
                        redundancy_seg = ["官方", "旗舰", "店", "苏宁", "自营"]
                        storename_seg = self.get_Seg("query",storenames[k])
                        storenames[k] = ''.join([i for i in storename_seg if i not in redundancy_seg])  # 将店铺名中的相关词去掉
                        if storenames[k] in keyword:  # 考虑keyword中命中了店铺名
                            keyword_new = keyword.replace(storenames[k],"")  # 去掉店铺名
                            qurey_segList = self.deal_QuerySeg(keyword_new)
                        if qurey_segList ==[] or keyword in storenames[k]:  # 考虑搜索词正好是店铺名称
                            HitRate_title = 1.0
                            HitRate_auxdescription = 1.0
                        else:
                            HitRate_title = self.count_HitRat(qurey_segList, titles[k])
                            HitRate_auxdescription = self.count_HitRat(qurey_segList, auxdescriptions[k])
                        hitrate = max(HitRate_title, HitRate_auxdescription)
                        if hitrate == 0:  # 若标题和卖点都没有中，考虑查看是否命中通子码信息
                            BjOtherTxt = self.check_HitBjOtherTxt(vonder_shops[k])
                            hitrate = self.count_HitRat(qurey_segList, ''.join(BjOtherTxt))
                        RateSum.append(hitrate)
                    AverageHitRate = sum(RateSum) / len(RateSum)
                    AverageHitRate = float("%.2f"%AverageHitRate)
                else:
                    titles = ["非常抱歉！没有找到与' *** ' 相关的商品。"]
                    RateSum = []
                    AverageHitRate = -1

            else:
                titles = ["根据相关法律法规和政策，无法显示相关的商品"]
                RateSum = []
                AverageHitRate = -1

            #************报告**************
            if 0 <= AverageHitRate <= 0.6:
                wordMatch = "fail"
                count += 1
                errorKey.append(keyword)
                if keyword.isdigit():  # 考虑qurey是商品编码的情况
                    partnumber = list(map(lambda x:x.split("-")[1],vonder_shops))
                    if partnumber.count(keyword) == len(partnumber) and partnumber != []:
                        wordMatch = "pass"
                        AverageHitRate = 1
                        RateSum = [1.0]*len(partnumber)
                        count = count-1
                        errorKey.pop()
            elif 0.6 < AverageHitRate <= 1:
                wordMatch = "pass"
            else:
                wordMatch = "warn"
            newTiles = list(map(lambda x:"<br>"+x,titles)) #为了报告中换行
            result.setKeyword(keyword)
            result.setWords(qurey_segList)
            result.setTitle(newTiles)
            result.setHitRate(RateSum)
            result.setAverageHitRate(AverageHitRate)
            result.setMatchStatus(wordMatch)
            self.searchresults3.append(result)
        return count,errorKey


































