#! usr/bin/env python
# -*- coding=utf-8 -*-

import json
import requests
import os
import time
import hashlib

apiKey = '8934031001776A04444F72154425DDBC'
headers = {"User-Agent":"Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)"}

def secretVal(param):
  timestamp= int(time.time()*1000)
  param['timestamp'] = timestamp
  keys = list(param.keys())
  keys.sort()

  strVal = ''
  for k in keys:
    strVal = strVal+k+str(param[k])

  strVal = apiKey+strVal+apiKey

  print('strVal: ' + strVal)
  mdf = hashlib.md5()
  mdf.update(strVal.encode(encoding='utf-8'))
  sign = mdf.hexdigest().upper()
  param['sign'] = sign
  return param


headers = {'Content-Type': 'application/json'}

req = requests.post(url = "http://test.dapengjiaoyu.com/api/bill/course-open", params=secretVal({"userId":"j7tsl3en"}),headers = headers, data= json.dumps([{"courseId":"k692nahhbp"},{"courseId":"k6940a46ip","stageId":"k6aetl35yz"}]))

print(req.request.url)
print(req.request.headers)
print(req.content.decode('UTF-8'))
print(req.status_code)
print(123)


