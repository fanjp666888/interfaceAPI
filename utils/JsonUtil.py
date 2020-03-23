import os
import json
from utils.Constant import Constant


class OperJson(object):
    def get_value(self, key, path=None):
        """读取要json文件,并根据给定的key返回值"""
        if path:
            assert "Not json dirName!!!!"
        date = self.read_json(path)
        return date.get(key)

    def read_json(self, path):
        """返回json全部内容"""
        with open(path, 'r', encoding='UTF-8') as f:
            data = json.loads(f.read())
        return data

OperJson = OperJson()
