import requests
import json


def post_request(url):
    # 创建列表
    items_list = []
    # post参数
    post_data = {
        "page": "1",
        "pageSize": "50",
        "keyWord": "",
        "cateList": "17",
        "sortType": "",
        "hasImage": "false",
        "ranNum": "0.29156731138582503"
    }
    # post 请求头
    req = requests.post(url, data=post_data)
    # 格式化json数据
    data = json.loads(req.text)
    print(req.request.body)

    # print(req.status_code)
    # print(req.text)
    # print(data)
    print(data['rows'][0])
    for i in range(len(data['rows'])):
        # print(tuple([data['rows'][i]['uuid'], data['rows'][i]['name']]))
        items_list.append(tuple([data['rows'][i]['uuid'], data['rows'][i]['name'],data['rows'][i]['culturalRelicNo']]))
    req.close()
    return items_list

if __name__ == '__main__':
    url = "https://zm-digicol.dpm.org.cn/cultural/queryList"
    post = post_request(url)
    print(post)
