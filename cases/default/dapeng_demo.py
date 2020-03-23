# encoding:utf-8
import json
import os
import datetime
import logging
import time
import unittest
from unittest import mock
from utils.LogSingleton import LogSingleton
from utils.Constant import Constant
from utils.ExcelUtil import ExcelUtil
from utils.RequestUtil import RequestUtil
from utils.JsonUtil import OperJson
from utils.ConfigUtil import ConfigUtil
from utils.DicKeyJsonUtil import json_search
# logger = LogSingleton().getInstance()
logger = logging.getLogger(Constant.LOGGER_NAME)


class YJDDCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        proDir = os.path.join(os.getcwd(), Constant.PATH_FOR_CONF)  # 动态获取配置文件目录相对路径
        headerPath = os.path.join(proDir, Constant.HEADER_FILE_NAME)  # 动态获取配置文件ini的相对路径
        cls.headers = OperJson.read_json(headerPath)
        cls._MockDate = OperJson.read_json(os.path.join(proDir, Constant.MOCK_FILE_NAME))
        config = ConfigUtil()
        cls.host = config.getRun("host")
        # logger.info(cls.host)


    @classmethod
    def tearDownClass(cls):
        pass

    # @unittest.skip('临时跳过test_commodity_type_judgment')
    def test_order_management_list(self):
        # hand_excel = ExcelUtil("\\Test.xlsx")
        hand_excel = ExcelUtil("\\订单-量管理.xlsx")
        rows = hand_excel.get_rows()
        for i in range(rows-1):
            data = hand_excel.get_rows_value(i + 1)  # 如果是第二个sheet,则加参数 index=1；有几个依次类推
            if data[5] == "yes":
                with self.subTest(i=i):
                    method = data[7]
                    url = self.host + data[8]
                    date = json.loads(data[9])
                    headers = json.loads(data[10])
                    if data[6] == "token":
                        headers["Authorization"] = ""
                    expect_status = json.loads(data[13])

                    # 使用mock数据
                    # mock_method = mock.Mock(return_value=get_value(url, '../config/mock_date.json'))
                    # request.request_main = mock_method
                    # res = request.request_main(method=method, url=url, data=post_data)
                    # 正常请求
                    logger.info("开始请求！！！！！！！！")
                    response = RequestUtil.request_main(method, url, date, headers)
                    logger.info("{0}-{1}-{2}-{3}状态码为：{4}".format(data[0], data[1], data[3], data[2], response.status_code))

                    result = response.json()
                    # logger.info(result)
                    for k in expect_status.keys():
                        # logger.info(str(expect_status[k]) + "," + str(json_search.search_key(result, k)))
                        self.assertIn(expect_status[k], json_search.search_key(result, k))











