import requests
import json
from utils.TokenUtil import get_token, refresh_token
sess = requests.Session()

web_url = "http://newtest.manager.dapengedu.net"


def get_api():
    api_url = "/of/payment/hisPage"

    headers = {
        "Authorization": "Bearer "+get_token(),
        # "Content-Type": "application/x-www-form-urlencoded",

    }
    res = requests.get(web_url+api_url, headers=headers)
    print(json.dumps(res.json(), indent=4))

#
# def add_user(token):
#     add_url = "user/system/core_user/add"
#     data = {"userId":"","phone":"15201022225","num":"ces003","userName":"ces003","pcAccount":"","userType":"0","password":"123546","collegeId":"j5m484vz","groupId":"","groupName":"","teamId":"","teamName":"","departmentId":"0c141ff6646f4fbda8fb4ec4f46ba4ef","departmentName":"推广四部","entryTime":"2019-10-31","departureTime":"","level":"1","roleId":2,"workingStatus":"1","status":"1"}
#     headers = {
#         "Authorization": "Bearer "+token,
#         "Content-Type": "application/json;charset=UTF-8"
#
#     }
#     res = requests.post(web_url+add_url, headers=headers, data=json.dumps(data))
#     print(res.text)


def mealId():
    """根据mealId获取商品详情"""
    # mock_url = "http://yapi.dapengjiaoyu.com/mock/154/quantity/system/zc_dist_batch/edit"
    url = "/goodsv2/v1/api/info/1340"
    headers2 = {
            "Authorization": "Bearer " + get_token(),
            "Content-Type": "application/json",
        }
    # data = {"mealId": "1322", }
    print(headers2)
    response = requests.get(web_url+url, headers=headers2)
    # response = requests.post(mock_url, headers=headers, data=json.dumps(data))
    print(response.status_code)
    print(json.dumps(response.json(), sort_keys=True, indent=4, ensure_ascii=False))



def KaiKe():
    """获取开课"""
    # mock_url = "http://yapi.dapengjiaoyu.com/mock/154/quantity/system/zc_dist_batch/edit"
    url = "/goodsv2/v1/api/item/1322"
    headers2 = {
            "Authorization": "Bearer " + get_token(),
            "Content-Type": "application/json",
        }
    data = {"startAmount": "1000", "endAmount":"2000"}
    print(headers2)
    response = requests.get(web_url+url, headers=headers2, params=data)
    # response = requests.post(mock_url, headers=headers, data=json.dumps(data))
    print(response.status_code)
    print(response.text)
    # print(json.dumps(response.json(), sort_keys=True, indent=4, ensure_ascii=False))


def School():
    """根据学院编号查询"""
    # mock_url = "http://yapi.dapengjiaoyu.com/mock/154/quantity/system/zc_dist_batch/edit"
    url = "/goodsv2/v1/api/school/j5m484vz"
    headers2 = {
            "Authorization": "Bearer " + get_token(),
            "Content-Type": "application/json",
        }
    data = {"p":"1", "ps":"2"}
    print(headers2)
    response = requests.get(web_url+url, headers=headers2, params=data)
    # response = requests.post(web_url+url, headers=headers2, data=json.dumps(data))
    print(json.dumps(response.json(), sort_keys=True, indent=4, ensure_ascii=False))


def activity():
    """根据主套餐获取活动"""
    # mock_url = "http://yapi.dapengjiaoyu.com/mock/154/quantity/system/zc_dist_batch/edit"
    url = "/goodsv2/v1/api/activity/item/1350"
    headers2 = {
            "Authorization": "Bearer " + get_token(),
            "Content-Type": "application/json",
        }
    data = {"startTime":"2020-03-04 00:00:00", "endTime":"2020-03-04 00:00:00"}
    print(headers2)
    response = requests.get(web_url+url, headers=headers2, params=data)
    # response = requests.post(web_url+url, headers=headers2, data=json.dumps(data))
    print(json.dumps(response.json(), sort_keys=True, indent=4, ensure_ascii=False))


if __name__ == '__main__':
    mealId()
    # KaiKe()
    # School()
    # activity()