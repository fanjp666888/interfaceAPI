#! /usr/bin/python3
# -*- coding: utf8 -*-
import json
import requests
from utils.ConfigUtil import ConfigUtil
from utils.Constant import Constant


class SegmentUtil(object):
    """分词工具集"""
    def __init__(self):
        self.headers = {"content-type":"application/json;charset=UTF-8"}
        config = ConfigUtil()
        self.segURL = config.getRun(Constant.CONFIG_PARAM_RUN_SEGMENTATION)    

    def getWordSegments(self, data):
        """根据关键词，获取分词后的结果"""
        response = requests.get(self.segURL, params=data)
        result = json.loads(response.text)
        segments = result['trans_res']
        words = []
        for segment in segments:
            words.append(segment['t']) 
        return words

    # 返回苏宁分词后的结果列表,#keyword = "美的小冰箱"
    def getSuningWordSegments(self, keyword):
        data = "q=%s&call_type=ST_PROB" % keyword
        words = self.getWordSegments(data) 
        return words

print(SegmentUtil().getSuningWordSegments("美的小冰箱"))