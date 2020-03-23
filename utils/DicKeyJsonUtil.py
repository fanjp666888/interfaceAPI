import json
"""
通过key匹配json文件中的value
"""

class json_search(object):
    '''通过key递归查询响应json'''
    def search_key(self, data, key):
        self.data = data
        self.key_value = []
        if self.data_json(data) != False:
            self.search(self.data, key)
            return self.key_value
        else:
            return False

    def data_json(self, data):
        ''' 入参判断'''
        '''json是str子类'''
        if isinstance(data, str):
            try:
                self.data = json.loads(data, encoding='utf-8')
            except ValueError:
                print("value error input")
                return False
        elif isinstance(data, dict):
            return self.data
        else:
            return False

    def search(self, data, key):
        for i in data:
            if i == key:
                self.key_value.append(data[i])
            elif isinstance(data[i], dict):
                self.search(data[i], key)
            elif isinstance(data[i], list):
                for j in data[i]:
                    if isinstance(j, dict):
                        self.search(j, key)

        return self.key_value

json_search = json_search()