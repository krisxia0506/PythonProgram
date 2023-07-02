# -*- coding: utf-8 -*-
# 获取浴室人数爬虫
import json

import pymysql
import requests


def getNewSession():
    url2 = 'http://h5cloud.17wanxiao.com:8080/CloudPayment/user/pay.do?versioncode=10556102&systemType=IOS&UAinfo=wanxiao&token=5c64d886-efb9-43ab-81f8-037276978059&customerId=104'
    res = requests.get(url2, allow_redirects=False)
    session = res.cookies.get("SESSION")
    return session


def get_list():
    url = "https://usewater.17wanxiao.com/api/use/water/h5/WXInvokFront/"

    headers = {
        "Host": "usewater.17wanxiao.com",
        "Accept": "application/json, text/plain, */*",
        "Sec-Fetch-Site": "same-origin",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Sec-Fetch-Mode": "cors",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Origin": "https://usewater.17wanxiao.com",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Wanxiao/5.7.0 CCBSDK/2.4.0",
        "Referer": "https://usewater.17wanxiao.com/schoolshower/index.html",
        "Content-Length": "124",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Cookie": "JSESSIONID=2aba5cc7-42dd-4396-850c-dfcdd45989dc;"
    }
    # 请求参数
    params = 'param=%7B%22cmd%22%3A%22zfbgetbathroomlist%22%2C%22outid%22%3A%22202007024220%22%2C%22timestamp%22%3A%2220230624222456%22%7D'

    r = requests.post(url, data=params, headers=headers)
    parsed_data = r.json()
    bathroom_list = parsed_data['body']
    bathroom_list = json.loads(bathroom_list)['data']['bathroomlist']
    result_list = []
    # 遍历浴室列表，提取需要的信息存储为字典，并添加到结果列表中
    for bathroom in bathroom_list:
        info = {
            "freetermnums": bathroom["freetermnums"],
            "sumtermnums": bathroom["sumtermnums"],
            "bathroomname": bathroom["bathroomname"]
        }
        result_list.append(info)
    return result_list


def creatConnect():
    db = pymysql.connect(host='58.87.95.28', user='xjy_database', password='F46YPJA8MH7PcKYE', charset='utf8',
                         db='xjy_database')
    cursor = db.cursor()
    return db, cursor


def insert(freetermnums, sumtermnums, bathroomname, db, cursor):
    sql = f"INSERT INTO bathroom_people (free, total, name,datetime) VALUES ({freetermnums},{sumtermnums},'{bathroomname}',now())"
    cursor.execute(sql)
    db.commit()


def closeConnect(db, cursor):
    cursor.close()
    db.close()


if __name__ == '__main__':

    bathroom_list = get_list()
    print(bathroom_list)
    db, cursor = creatConnect()
    for bathroom in bathroom_list:
        insert(bathroom['freetermnums'], bathroom['sumtermnums'], bathroom['bathroomname'], db, cursor)
    closeConnect(db, cursor)
    # 在每天你的11点到12点之间，每隔5分钟执行一次
    # crontab -e
    # 0/1 11-23 * * * python3 /root/HttpRequest/bathroom_people.py
    # 查看cat /var/spool/mail/root
