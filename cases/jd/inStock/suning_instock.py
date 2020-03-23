#! /usr/bin/python3
# -*- coding: utf8 -*-
import urllib.parse,re,datetime,logging,unittest,threading,os,multiprocessing
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from dp_interface.utils.LogSingleton import LogSingleton
from dp_interface.utils.Constant import Constant
from dp_interface.utils.SpiderUtil import SpiderUtil
from dp_interface.utils.ConfigUtil import ConfigUtil
from dp_interface.utils.KeywordUtil import KeywordUtil
from dp_interface.utils.ExcelUtil import ExcelUtil
from dp_interface.utils.ReportUtil_instock import ReportUtil
from dp_interface.format.suning.SearchResult import SearchResult

logger = LogSingleton().getInstance()
logger = logging.getLogger(Constant.LOGGER_NAME)

class inStock(unittest.TestCase):
    dict_outcome = {}
    CHECK_RANDOM_KEYWORD_NUM = 20
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

            file_path = os.path.join(os.getcwd(), Constant.PATH_FOR_FILES)

            file_abspath = os.path.join(file_path, "topQuery_suning_1million.txt")
            self.ku = KeywordUtil(file_abspath)

    @classmethod
    def tearDownClass(self):
        if self.writeExcelFlag:
            self.stopTime = datetime.datetime.now()
            duration = str(self.stopTime - self.startTime)
            startTime = str(self.startTime)[:19]
            duration = duration[:duration.find(".")]
            reportUtil = ReportUtil()

            reportUtil.generateReport(startTime, duration, self.searchresults)
            excel = ExcelUtil()
            excel.exportToExcel_instock("Instock_"+startTime.replace(" ", "_").replace(":", "-", 2), self.searchresults)
        logger.info("---end test suite(%s)---" % __name__)

    def test_inStock(self):
        """ 测试勾选有货后，是否会展现出来无货或不可销售的商品"""
        keywords = self.ku.getRandomKeywords(self.CHECK_RANDOM_KEYWORD_NUM)
        # keywords = ["史密斯热水器 149升","智利进口车厘子5kg"]
        # keywords = ["冰箱","空调","洗衣机","电视"]
        # keywords = ["冰箱"]
        self.all_abnormal = []
        lastResult =self.multi_Proccess(keywords)
        self.searchresults.extend(lastResult[0])
        self.all_abnormal.extend(lastResult[1])
        assert len(self.all_abnormal) == 0

    def get_VarParam(self, url,keyword):

        """通过首次搜索获取网页源代码中的var param数据，此数据用于构建异步加载的链接"""

        Soup = SpiderUtil.getSoupContent(url + urllib.parse.quote(keyword) + "/" + "&iy=1")
        if Soup != "":
            scripts = Soup.find_all("script", type="text/javascript")
            for script in scripts:
                if len(script.contents) > 0:
                    if "var param" in str(script.contents[0]).strip():
                        # logger.info("要找的：" + str(script.contents[0]).strip())
                        content_list = str(script.contents[0]).strip().split(";")  # 分割为[var param,param.sortType,param.inventory]
                        # 此处循环是将整个字符串分割存储为字典的形式
                        for element in content_list[0][13:-1].split(","):  # 无法使用json.loads
                            dic_list = element.strip().split(":")
                            if "\"" not in dic_list[1].strip() and "\'" not in dic_list[1].strip():
                                dic = {eval(dic_list[0]): dic_list[1].strip()}
                            else:
                                dic = {eval(dic_list[0]): eval(dic_list[1].strip())}
                            self.dics.update(dic)
                        # 此处循环是将后续的字符串以列表的形式存放
                        for element in content_list[1:]:
                            if len(element) > 0:
                                self.lists.append(re.search(r'\".+\"', element.strip()).group(0)[1:-1])
        else:
            pass
            #出现error，优化

    def get_SearchUrl(self,keyword):
        """根据网页源代码中的var parm的信息，来模拟异步加载商品(XHR)的链接"""
        #将固定的信息加入链接中
        url_join = "http://search.suning.com/emall/searchV1Product.do?keyword="+urllib.parse.quote(keyword)+"&pg=01&isNoResult=0&id=IDENTIFYING&sub=0&iy=1"
        join_list = ["categoryId", "isList", "st", "n", "sesab", "lesCityId", "numFound"]
        for i in join_list:
            if i in self.dics.keys():
                if i == "categoryId":
                    url_join += "&ci=" + self.dics["categoryId"]
                elif i == "isList":
                    url_join += "&il=" + self.dics["isList"]
                elif i == "lesCityId":
                    url_join += "&cc=" + self.dics["lesCityId"]
                elif i == "numFound":
                    url_join += "&jzq=" + self.dics["numFound"]
                else:
                    url_join += "&"+i+"="+self.dics[i]
        for j in self.lists:
            url_join += j
        return url_join

    def get_Inv(self, vonder_shop_id):
        vonder_id = vonder_shop_id.split("-")[0]
        shop_id = vonder_shop_id.split("-")[1]
        if len(vonder_id) < 10:  # 将店铺id补满10位
            vonder_idnew = "0" * (10 - len(vonder_id)) + vonder_id
        else:
            vonder_idnew = vonder_id
        if len(shop_id) < 18:  # 将商品id补满18位
            shop_idnew = "0" * (18 - len(shop_id)) + shop_id
        else:
            shop_idnew = shop_id
        url = r"https://icps.suning.com/icps-web/getVarnishAllPrice014/{}_{}_{}0101_{}_1_getClusterPrice.vhtm?callback=getClusterPrice".format(
            shop_idnew, self.lesCityId, self.lesCityId, vonder_idnew)
        logger.info("验证售货状态url%s"%url)
        # logger.info(threading.current_thread().name+multiprocessing.current_process().name)
        html = SpiderUtil.getHtml(url)
        inv = re.findall(r'"invStatus":"(.*?)"', html)  # invStatus 对应的值
        if inv != []:
            # invStatus=1 是正常商品，invStatus=4 是延迟发货商品,
            # 预约品的状态有时也等于2，判断是预约品还是无货品
            if int(inv[0]) != 1 and int(inv[0]) != 4:
                self.list_clock.acquire()
                self.abnormal_tmp.append(vonder_shop_id)
                self.list_clock.release()
            return inv[0]
        else:
            return None

    def check_Status(self,keyword,page_list,url_join):
        """
        cp：具体的第多少页，从0开始，每页最多120个品，paging：cp每页分为4小页，每页30个品。
        :param page_list:由页数组成列表
        :param url_join:每页30个品，模拟链接
        :return:None
        """
        vender_shop_thread = []
        for page in page_list:
            for subPage in range(4):
                URL = url_join + "&cp=" + str(page) + "&paging=" + str(subPage)
                logger.info("当前线程%s，query=%s,拼接link：%s"%(threading.current_thread().name,keyword,URL))
                response = SpiderUtil.getHtml(URL)
                self.list_clock.acquire()
                vender_shop_thread.extend(re.findall(r'<li docType="1".*id="(.*?)"', response) + re.findall(r'<div.*product-box  basic.*id="(.*?)"', response))
                self.list_clock.release()
        InvStatus_thread = list(map(self.get_Inv, vender_shop_thread))
        self.list_clock.acquire()
        self.invStatus.extend(InvStatus_thread)
        self.vender_shop.extend(vender_shop_thread)
        self.list_clock.release()

    def check_DetailInfo(self,abnormal_tmp):
        """
        通过模拟浏览器的方式，得到商品的确切信息
        :param inv: 存货状态，
               invStatus: "3" : 暂不销售
               invStatus: "2" : 上海无货，  还有预约的情况
               invStatus: "1" : 有货
               invStatus: "4" :可以加入购物车下单，四季页提示：备货中
        :param vonder_id: 商户编码
        :param shop_id: 商品编码
        :return: 返回false：异常商品，返回true：正常商品
        """

        browser = webdriver.Chrome(executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        # browser.set_page_load_timeout(30)  # 自行设置加载时间,# 在运行中，处理浏览器卡死的情况
        try:
            browser.get("http://product.suning.com/" + abnormal_tmp[0].split("-")[0] + "/" + abnormal_tmp[0].split("-")[1] + ".html")
            browser.add_cookie({
                'domain': '.jd.com',
                'httpOnly': False,
                'name': 'cityId',
                'path': '/',
                'secure': False,
                'value': self.dics["cityId"]
            })  # 设置浏览器默认的发货城市
            browser.refresh()
        except Exception as e:
            pass
        for vonder_shop in abnormal_tmp:
            vonder_id = vonder_shop.split("-")[0]
            shop_id = vonder_shop.split("-")[1]
            tag = 0
            lab_except = 0 # 1表示异常情况，0 表示正常情况
            while True:
                try:
                    browser.get("http://product.suning.com/" + vonder_id + "/" + shop_id + ".html")
                    try:
                        elements = browser.find_elements_by_tag_name("h5")  # 非常抱歉！没有找到相关商品
                        for element in elements:
                            if element.text == "很抱歉,此商品不存在!":
                                tag = 1
                                lab_except = 0
                                break
                    except NoSuchElementException as e:
                        tag = 0
                    if tag == 0:
                        lab_addcart = self.isElementExist(browser, "addCart")
                        lab_nowadd = self.isElementExist(browser, "buyNowAddCart")
                        if lab_addcart[0] and lab_addcart[1]:
                            lab_except = 0
                        elif lab_nowadd[0] and lab_nowadd[1]:
                            lab_except = 0
                        else:
                            lab_except = 1
                    break
                except Exception as e:
                    continue
            if lab_except == 1:
                self.list_clock.acquire()
                self.abnormal.append(vonder_shop)
                self.list_clock.release()
        browser.quit()

    def isElementExist(self,browser,id):
        flag=True
        try:
            element = browser.find_element_by_id(id)
            display = element.is_displayed()  # 若是显示的，则为true，否则为false
        except:
            flag=False
            display=False
        return flag,display

    def multi_Thread(self,keywords,result_AllProcess,abnormal_AllProcess):
        """
        每个keyword按照页数分割，进行多线程
        :param word: 关键词
        :return: None
        """
        url = "http://search.suning.com/"

        for keyword in keywords:
            self.abnormal_tmp = []
            result = SearchResult()
            self.dics = {}  # 将var param所有的参数以字典的形式存放
            self.lists = []  # 将param.sortType = "&st=0";直接以列表的形式存放
            self.vender_shop = []  # 存储爬取到的所有商品
            self.invStatus = []  # 存储商品的有无货的状态
            self.abnormal = []  # 存储异常商品的信息
            self.get_VarParam(url, keyword)
            url_join = self.get_SearchUrl(keyword)
            self.lesCityId = self.dics["lesCityId"]
            page_list = range(int(self.dics["pageNumbers"]))
            print(page_list)
            # 多线程
            threads = []
            pthreadOfNumb = 4# 线程数
            self.list_clock = threading.Lock()
            for threadsNumber in range(pthreadOfNumb):
                key_seg = page_list[threadsNumber::pthreadOfNumb]
                temp = threading.Thread(target=self.check_Status, args=(keyword,key_seg, url_join,))
                threads.append(temp)
            for t in threads:
                t.setDaemon(True)
                t.start()
            for t in threads:
                t.join()
            logger.info("搜索query=%s召回商品的个数：%s"%(keyword,len(self.vender_shop)))
            logger.info("搜索query=%s召回商品可售不可售状态的个数：%s"%(keyword,len(self.invStatus)))
            # logger.info(self.invStatus)
            # logger.info(self.abnormal)
            if self.abnormal_tmp != []:
                self.check_DetailInfo(self.abnormal_tmp)
            #***********detail报告****************
            Len = len(self.abnormal)
            if Len == 0:
                wordMatch = "pass"
            else:
                wordMatch = "fail"
            result.setKeyword(keyword)
            result.setPageNum(self.dics["pageNumbers"])
            result.setTotalCount(self.dics["numFound"])
            result.setUnmatched(self.abnormal)
            result.setMatchStatus(wordMatch)
            result_AllProcess.append(result)
            abnormal_AllProcess.extend(self.abnormal)

    def multi_Proccess(self,words):
        with multiprocessing.Manager() as MG:  # 重命名
            result_AllProcess = multiprocessing.Manager().list()  # 主进程与子进程共享这个List
            abnormal_AllProcess = multiprocessing.Manager().list()
            process_list = []  # 记录进程列表
            cpu_count = multiprocessing.cpu_count()  # 计算电脑的核数
            # cpu_count = int(cpu_count/2)
            for i in range(cpu_count):
                keys = words[i::cpu_count]
                process = multiprocessing.Process(target=self.multi_Thread,args=(keys,result_AllProcess,abnormal_AllProcess))
                process.start()
                process_list.append(process)
            for p in process_list:
                p.join()
        return result_AllProcess,abnormal_AllProcess

    def __getstate__(self):
        self.dict_outcome = self.__dict__.copy()
        del self.dict_outcome['_outcome']
        return self.dict_outcome

    def __setstate__(self, state):
        self.__dict__.update(self.dict_outcome)


    # def tmp_test_check_again(self):
    #     """相隔3个小时，对商品再次检测商品是否还在有货之中，
    #     将结果还写到detail的报告中
    #     """
    #     self.writeExcelFlag = False
    #     start = time.time()
    #     file_path = os.path.join(os.getcwd(), Constant.PATH_FOR_REPORTS)
    #     filename = "detailed_2019-03-08-16_09_13.html"  # 成熟之后，以后优化
    #     file_abspath = os.path.join(file_path, filename)
    #     logger.debug(file_abspath)
    #     with open(file_abspath,'r+',encoding='utf-8') as html:
    #         htmlhandle = html.read()
    #         soup = BeautifulSoup(htmlhandle,"lxml")#需要安装lxml包
    #         tds = soup.find_all("td",type="unmatched")
    #         logger.info(tds)
    #         for td in tds:
    #             for n in str(td.string)[2:-1].split(","):
    #                 vendor_shop = n[1:-1]
    #                 partnumber = vendor_shop.split("-")[1]
    #                 issue = []
    #                 url = "https://search.suning.com/" + partnumber + "/&iy=1"
    #                 soup = SpiderUtil.getSoupContent(url)
    #                 h3 = soup.find_all("h3")
    #                 tag = 0
    #                 for h in h3:
    #                     if h.string == "非常抱歉！没有找到符合条件的商品":
    #                         tag = 1
    #                         break
    #                 if tag == 0:
    #                     li_list = soup.find_all("li", doctype="1")
    #                     print("li_list",li_list)
    #                     for li in li_list:
    #                         if li.has_attr("id"):  # 当时有套餐品的时候，li中没有id信息
    #                             id = li["id"]
    #                         else:
    #                             div = li.find("div", class_=re.compile("product-box basic.*"))
    #                             id = div["id"]
    #                         if id == vendor_shop:
    #                             issue.append(vendor_shop)
    #                             break
    #                 end = time.time()
    #                 first_TMPL = r"""
    #                                 <p class='attribute'><strong>开始时间 : </strong> %(starttime)s</p>
    #                                 <p class='attribute'><strong>合计耗时 : </strong> %(duration)s</p>
    #                                 <table id='last result' class="table table-condensed table-bordered table-hover">
    #                                 <tr id='header' class="text-center success" style="font-weight: bold;font-size: 14px;">
    #                                     <td>再次验证结果</td>
    #                                     <td>问题商品</td>
    #                                 </tr>
    #                                 """
    #                 second_TMPL = r"""
    #                                  <tr class='last test'>
    #                                  <td style="vertical-align:middle; text-align:center"><img width="20" height="20" src="../img/%(status)s.jpg"></td>
    #                                  <td style="vertical-align:middle; text-align:center" class="unmatched"> %(issue)s</td>
    #                                  </tr>
    #                                  """
    #                 StartTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start))
    #                 Duration = time.strftime("%M:%S", time.localtime(end-start))
    #                 print("issue",issue)
    #                 if len(issue) == 0:
    #                     status = "pass"
    #                 else:
    #                     status = "fail"
    #                 first = first_TMPL % dict(starttime=StartTime, duration=Duration)
    #                 seond = second_TMPL % dict(status=status, issue=issue)
    #                 html.seek(0)
    #                 lines = html.readlines()
    #                 lines.insert(len(lines) - 7,first+seond )
    #                 s = "".join(lines)
    #                 html.seek(0)
    #                 html.write(s)










