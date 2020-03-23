import requests
import json
web_url = "http://newtest.manager.dapengedu.net/"


def get_token(refresh_token=None):
    """获取token"""
    sess = requests.Session()
    sess.auth = ('dapengbeijingservice', 'secretservice')  # 获取token的UserName/Password码
    token_url = "oauth/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "password",
        "username": "18800000000",
        "password": "123456",
        "scope": "serviceclient"
    }
    res = sess.post(web_url+token_url, headers=headers, data=data)
    if refresh_token:
        return res.json().get("refresh_token")
    return res.json().get("access_token")


def refresh_token():
    """刷新token"""
    sess = requests.Session()
    sess.auth = ('dapengbeijingservice', 'secretservice')
    mock_url = "http://yapi.dapengjiaoyu.com/mock/121http://tongshang"
    token_url = "oauth/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    token = get_token("refresh_token")
    data = {"grant_type": "refresh_token",
            "refresh_token": token
            }
    res = sess.post(web_url+token_url, headers=headers, data=data)
    # print(res.status_code)
    # print(res.text)
    return res.json().get("access_token")


# print(refresh_token())