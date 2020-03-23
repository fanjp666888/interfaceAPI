#! /usr/bin/python3
# -*- coding: utf8 -*-
import logging
import unittest
import os
import datetime
import random
import time
import re
from utils.Constant import Constant
from utils.KeywordUtil import KeywordUtil
from utils.RequestUtil import RequestUtil
from utils.ConfigUtil import ConfigUtil
from utils.ReportUtil_sort import ReportUtil_sort
from utils.ExcelUtil import ExcelUtil
from format.suning.SearchResult import SearchResult
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


logger = logging.getLogger(Constant.LOGGER_NAME)
req = RequestUtil()
config = ConfigUtil()



class PriceSort(unittest.TestCase):
    all_sort_results = []
    ascending_or_descending = ''

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
        self.stopTime = datetime.datetime.now()
        duration = str(self.stopTime - self.startTime)
        startTime = str(self.startTime)[:19]
        duration = duration[:duration.find(".")]
        reportUtil = ReportUtil_sort()
        reportUtil.generateReport(startTime, duration, self.all_sort_results)
        excel = ExcelUtil()
        excel.export_price_sort_test_result_to_excel('pricesort_test_result.xls', self.all_sort_results)
        logger.info("---end test suite(%s)---" % __name__)

    def unavailable_or_not_sale_flag(self, browser, i):
        # xpath = '//*[@class="general clearfix"]/li[%s]/div/div/div[1]/div/span/em' % (i + 1)
        xpath = '//*[@class="product-list  clearfix"]/ul/li[%s]/div/div/div[1]/div/span/em' % (i + 1)
        """
        flag=0，有货且销售
        flag=1，不销售或无货
        """
        flag = 0
        if len(browser.find_elements_by_xpath(xpath)) != 0:
            page_flag = browser.find_element_by_xpath(xpath).text
            if page_flag == '本地暂不销售' or '无货' in page_flag:
                flag = 1
        return flag

    def get_commodity_price(self, browser, i):
        # xpath = '//*[@class="general clearfix"]/li[%s]' % (i + 1)
        # xpath = '//*[@class="fashion clearfix"]/li[%s]' % (i + 1)
        xpath = '//*[@class="product-list  clearfix"]/ul/li[%s]' % (i + 1)
        commodity_info = str(browser.find_element_by_xpath(xpath).text)
        if '¥' in commodity_info:
            commodity_price_info = commodity_info.split('¥')[1]
            # logger.info(commodity_price_info)
            '''获取不到商品价格时，commodity_price为-1，例如商品价格为？？？'''
            if_commodity_price_exit = re.search('\d+([.]\d)?', commodity_price_info)
            if if_commodity_price_exit is None:
                commodity_price = -1
            else:
                commodity_price = float(if_commodity_price_exit.group())
        else:
            commodity_price = -1
        # logger.info(commodity_price)
        return commodity_price

    def sort_determine(self, browser, Keyword):
        result = SearchResult()
        set_sort_result_detail = ''
        price = 0
        sort_error_flag = 0
        unavailable_or_not_sale_exist_flag = 0
        browser.find_element_by_xpath('//*[@id="second-filter"]/div[1]/div[1]/span[4]/em').click()
        time.sleep(2)
        """获取排序规则，是从小到大还是从大到小"""
        collation = browser.find_element_by_xpath('//*[@id="second-filter"]/div[1]/div[1]/span[4]/em/i').get_attribute(
            'class')
        """获取当前页面加载的产品数量"""
        commodity_num = len(browser.find_elements_by_xpath('//*[@doctype="1"]'))
        browser.set_window_size(1300, 30000)
        browser.execute_script("window.scrollBy(0,3000)")
        time.sleep(2)
        # element = WebDriverWait(browser, 10).until(lambda driver: driver.find_element_by_id("kw"))
        if collation == 'price sx':
            self.ascending_or_descending = '升序'
            for i in range(commodity_num):
                unavailable_or_not_sale_flag = self.unavailable_or_not_sale_flag(browser, i)
                if unavailable_or_not_sale_flag == 0:
                    commodity_price = self.get_commodity_price(browser, i)
                    '''获取不到商品价格时，commodity_price为-1'''
                    if commodity_price == -1:
                        continue
                    if unavailable_or_not_sale_exist_flag == 0:
                        if price == 0:
                            price = commodity_price
                        else:
                            if commodity_price >= price:
                                price = commodity_price
                            else:
                                sort_error_flag += 1
                                logger.info(Keyword + "排序错误，第%s个产品价格排序错误" % str(i + 1))
                                set_sort_result_detail = set_sort_result_detail + "第%s个产品价格排序错误" % str(
                                    i + 1) + '<br>'
                    else:
                        sort_error_flag += 1
                        logger.info(Keyword + "排序错误，第%s个产品价格排序错误，有货销售产品排在无货或者暂不销售的商品后面" % str(i + 1))
                        unavailable_or_not_sale_exist_flag -= 1
                        set_sort_result_detail = set_sort_result_detail + "第%s个产品价格排序错误，有货销售产品排在无货或者暂不销售的商品后面" % str(
                            i + 1) + '<br>'
                else:
                    unavailable_or_not_sale_exist_flag = 1
        elif collation == 'price jx':
            self.ascending_or_descending = '降序'
            for i in range(commodity_num):
                unavailable_or_not_sale_flag = self.unavailable_or_not_sale_flag(browser, i)
                if unavailable_or_not_sale_flag == 0:
                    commodity_price = self.get_commodity_price(browser, i)
                    if commodity_price == -1:
                        continue
                    if unavailable_or_not_sale_exist_flag == 0:
                        if price == 0:
                            price = commodity_price
                        else:
                            if commodity_price <= price:
                                price = commodity_price
                            else:
                                sort_error_flag += 1
                                logger.info(Keyword + "排序错误，第%s个产品价格排序错误" % str(i + 1))
                                set_sort_result_detail = set_sort_result_detail + "第%s个产品价格排序错误" % str(i + 1) + '<br>'
                    else:
                        sort_error_flag += 1
                        logger.info(Keyword + "排序错误，第%s个产品价格排序错误，有货销售产品排在无货或者暂不销售的商品后面" % str(i + 1))
                        unavailable_or_not_sale_exist_flag -= 1
                        set_sort_result_detail = set_sort_result_detail + "第%s个产品价格排序错误，有货销售产品排在无货或者暂不销售的商品后面" % str(i + 1) + '<br>'
                else:
                    unavailable_or_not_sale_exist_flag = 1
        else:
            sort_error_flag += 1
        if sort_error_flag != 0:
            test_result = 'fail'
            result.set_sort_result_detail(set_sort_result_detail)
        else:
            test_result = 'pass'
        result.set_sort_result_detail(set_sort_result_detail)
        result.setKeyword(Keyword)
        result.set_sort_result(test_result)
        result.set_sort_type('价格' + self.ascending_or_descending)
        self.all_sort_results.append(result)

    def test_priceSort(self):
        """ 测试勾选价格排序后，是否有排序错误的商品"""
        browser = webdriver.Chrome()
        keywords = self.all_keywords
        url = 'http://search.suning.com/%s/' % keywords[0]
        # url = 'http://search.suning.com/手机/'
        browser.get(url)
        if 'ssdsn_search_egg_close' in browser.page_source:
            browser.find_element_by_xpath('//*[@id="pop418"]/a').click()
        """点击按价格排序"""
        for Keyword in random.sample(keywords, 100):
        # for Keyword in keywords:
            logger.info(Keyword)
            browser.find_element_by_xpath('// *[ @ id = "searchKeywords"]').clear()
            browser.find_element_by_xpath('// *[ @ id = "searchKeywords"]').send_keys(Keyword)
            browser.find_element_by_xpath('//*[@id="searchSubmit"]').click()
            time.sleep(1)
            if '试用品详情' in browser.page_source:
                browser.back()
                continue
            if '免费试用' in browser.page_source:
                browser.back()
                continue
            if '众筹' in browser.page_source:
                browser.back()
                continue
            if '非常抱歉！没有找到与' in browser.page_source:
                browser.back()
                continue
            if 'ssdsn_search_egg_close' in browser.page_source:
                browser.find_element_by_xpath('//*[@id="pop418"]/a').click()
            if '全部商品分类' not in browser.page_source:
                browser.back()
                continue
            if '全部结果' not in browser.page_source:
                browser.back()
                continue
            self.sort_determine(browser, Keyword)
            # 滑动到顶部
            js = "window.scrollTo(0,100)"
            browser.execute_script(js)
            self.sort_determine(browser, Keyword)
        browser.close()