#! /usr/bin/python3
# -*- coding: utf8 -*-
import json
import requests
from json.decoder import JSONDecodeError
from utils.ConfigUtil import ConfigUtil
from utils.TokenUtil import get_token
import logging
from utils.Constant import Constant
logger = logging.getLogger(Constant.LOGGER_NAME)


class RequestUtil(object):
    """封装请求模块"""
    # def __init__(self):
    #     self.headers = {"content-type": "application/json;charset=UTF-8", "Connnection": "close"}
    #
    # def get(self, url):
    #     """Get请求，返回json格式的结果"""
    #     requests.adapters.DEFAULT_RETRIES = 5
    #     session = requests.session()
    #     session.keep_alive = False
    #     response = requests.get(url, timeout=10)
    #     result = json.loads(response.text)
    #     return result
    #
    # def post(self, url, data):
    #     """Post请求，返回json格式的结果"""
    #     requests.adapters.DEFAULT_RETRIES = 5
    #     response = requests.post(url, data=data, headers=self.headers, timeout=10)
    #     try:
    #         result = json.loads(response.text)
    #     except JSONDecodeError:
    #         result = ""
    #     return result

    def request_get(self, url, headers, params=None, **kwargs):
        """get请求"""
        if params:
            response = requests.get(url, params=params, headers=headers, timeout=5, **kwargs)
        else:
            response = requests.get(url, headers=headers, timeout=5, **kwargs)
        return response

    def request_post(self, url, headers, data=None, **kwargs):
        """post请求"""
        if isinstance(data, dict):
            response = requests.post(url, data=json.dumps(data), headers=headers, timeout=5, **kwargs)
        else:
            response = requests.post(url, data=data, headers=headers, timeout=5, **kwargs)
        return response

    def request_delete(self, url, headers, data=None, **kwargs):
        return requests.delete(url, data=data, headers=headers, timeout=5, **kwargs)


    @classmethod
    def request_main(cls, method, url, data=None, headers=None, **kwargs):
        """
        :param method: 请求类型
        :param url: 请求链接
        :param data: 参数
        :param kwargs: 其他参数
        :return: response
        """
        # base_url = ConfigUtil().getRun("host")
        # if "http" not in url:
        #     url = base_url + url
        # print(url)
        if isinstance(headers, dict) and "Authorization" in headers.keys():
            headers["Authorization"] = "Bearer " + get_token()
        if method == "GET":
            response = cls().request_get(url, headers=headers, params=data, **kwargs)
        elif method == "DELETE":
            response = cls().request_delete(url, headers=headers, params=data, **kwargs)
        else:
            response = cls().request_post(url, headers=headers,  data=data, **kwargs)

        return response

RequestUtil = RequestUtil()