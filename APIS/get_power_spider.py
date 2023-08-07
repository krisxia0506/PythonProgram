"""
此段代码用于爬取电力数据
宿舍楼和房间号从数据库中获取
总共耗时02时39分20秒
总共耗时02时39分08秒
总共耗时02时38分43秒
总共耗时02时38分02秒
总共耗时02时38分47秒
version: 1.1
created by: XiaJiayi
created on: 2023/7/30
modify on: 2023/8/7
"""
import random
import time
import warnings

import pymysql
import requests

session_value = 'null'
# 开始时间
start_time = time.time()
# 结束时间
end_time = ''

proxies = {
    # 'http': 'http://114.232.109.207:8888'
}


# 数据库连接
def creat_connect():
    db = pymysql.connect(host='58.87.95.28', user='APIS', password='CmaPzyaGAetzezyY', charset='utf8', db='apis')
    cursor = db.cursor()
    return db, cursor


# 关闭数据库连接
def close_connect(db, cursor):
    cursor.close()
    db.close()


# 获取token
def get_token():
    db, cursor = creat_connect()
    sql = "SELECT token FROM token WHERE id = 1"
    cursor.execute(sql)
    results = cursor.fetchall()
    close_connect(db, cursor)
    return results[0][0]  # 02afcb54-5512-4896-8d77-f1cb1035ccb3


# 获取session
def getNewSession() -> object:
    url2 = 'http://h5cloud.17wanxiao.com:8080/CloudPayment/user/pay.do?versioncode=10556102&systemType=IOS&UAinfo=wanxiao&token=' + get_token() + '&customerId=104'
    res = requests.get(url2, allow_redirects=False)
    session = res.cookies.get("SESSION")
    return session  # d9002a26-2106-4f07-9ba0-be00bf0707a2


# 通过数据库获取所有的宿舍楼和房间号
def getBuildIDAndRoomID():
    db, cursor = creat_connect()
    sql = "SELECT buildID,roomID FROM roomid"
    cursor.execute(sql)
    results = cursor.fetchall()
    close_connect(db, cursor)
    for item in results:
        yield item  # (1,101)


# 获取日期为昨天的最后一条记录，用于断点爬取
def get_last_record():
    db, cursor = creat_connect()
    sql = "SELECT * FROM powertable WHERE date(`date`) = CURDATE() - INTERVAL 1 DAY ORDER BY `id` DESC LIMIT 1;"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        # 如果没有结果，表示还没开始爬取，返回1,101
        if len(results) == 0:
            return None
        else:
            return results[0][1], results[0][2]
    except Exception as e:
        print("获取最后一条记录出现异常，异常信息如下\n", e)
        return None
    finally:
        close_connect(db, cursor)


# 断点续爬,id_gen是所有宿舍号
def continuously_climbing_at_breakpoints(id_gen):
    print("判断是否需要断点续爬")
    last_rec = get_last_record()
    # 如果get_last_record()返回了none，说明没有昨天的数据，需要从头爬取
    if last_rec:
        print("需要断点续爬，最后一条数据是{}".format(last_rec))
        for x in id_gen:
            if x == last_rec:
                break
        for x in id_gen:
            yield x
    else:
        print("不需要断点续爬，从头开始爬取")
        for x in id_gen:
            yield x


# 获取电量
def get_power(build, room, session):
    # 睡眠随机时间，毫秒级
    time.sleep(random.uniform(2, 4))
    # 10-635需要特殊处理
    if build == 10 and room == 636:
        room = 635
    # 楼号转义
    building_id2post = {
        1: '1-9--10-',
        2: '1-10--11-',
        3: '1-11--12-',
        4: '1-12--9-',
        5: '1-3--3-',
        6: '1-1--1-',
        7: '1-4--8-',
        8: '1-5--4-',
        9: '1-6--5-',
        10: '1-7--6-',
        11: '1-8--7-'
    }
    url = f'http://h5cloud.17wanxiao.com:8080/CloudPayment/user/getRoomState.do?' \
          f'payProId=2124&schoolcode=104&businesstype=2&roomverify={building_id2post[build]}{room}'

    header = {
        "Host": "h5cloud.17wanxiao.com:8080",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Wanxiao/5.5.6 CCBSDK/2.4.0",
        "Accept": "application/json",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip,deflate",
        "Referer": "http://h5cloud.17wanxiao.com:8080/CloudPayment/bill/selectPayProject.do?txcode=2&interurl=substituted_pay&payProId=2124&amtflag=0&payamt=0&payproname=%E8%B4%AD%E7%94%B5&img=http://cloud.17wanxiao",
        "Connection": "keep-alive"
        ,
        "Cookie": f'SESSION={session}; SERVERID=e8e02aa88506006460462b373a5d91a9|1653700198|1653700055'
    }
    try:
        r = requests.post(url, headers=header, proxies=proxies)
        print("此次请求的响应内容为-->", r.text)
    except:
        print("请求失败，尝试重新请求")
        get_power(build, room, session)
    try:
        if r.text == 'RspBaseVO [code=ERROR, msg=系统繁忙，请稍后重试, subCode=null, subMsg=null]':
            return 'error', 'sessionError'
        elif r.json()['returncode'] == '100':
            return 'success', r.json()['quantity']
        elif r.json()['returncode'] == 'FAIL':
            return 'error', 'noRoom'
        else:
            return 'error', 'otherError'
    except:
        return 'error', 'otherError'


# 对power方法做一个细节判断
def before_power(build, room, session):
    global session_value
    power_result = get_power(build, room, session)
    print("power_result的返回值-->", power_result)
    if power_result[0] == "error":
        if power_result[1] == 'sessionError':
            print("\033[91msession过期了，准备获取新session，并重新查询\033[0m")
            session_value = getNewSession()
            print("获取到了新的session", session_value)
            power_result = get_power(build, room, session_value)
            return power_result[1]
    elif power_result[0] == 'success':
        return power_result[1]
    else:
        return "其它情况"


# 插入数据 2023-08-2 23:59:00
def insert(buildingID, roomID, power_data, db, cursor):
    sql = f"INSERT INTO powertable (buildingID,roomID,power,date) VALUES ({buildingID},{roomID},{power_data},date_sub(CURDATE(),interval 1 minute ))"
    # 尝试插入3次
    i = 0
    while i < 3:
        try:
            cursor.execute(sql)
            print("\033[92m数据插入成功\033[0m")
            break
        except Exception as e:
            if "Duplicate entry" in str(e):
                print("\033[91m唯一索引异常，数据已存在插入失败，跳过此次插入\033[0m")
                break
            else:
                print("插入失败，尝试重新插入第{}次".format(i + 1))
                i += 1
    else:
        print("\033[91m 已重试3次，插入仍然失败，跳过此次插入\033[0m")
    db.commit()


def main():
    # 获取数据库连接
    db, cursor = creat_connect()
    # 遍历getBuildIDAndRoomID()的结果
    for item in continuously_climbing_at_breakpoints(getBuildIDAndRoomID()):
        try:
            print("——————————————————————这是分隔符—————————————————————")
            print("此次请求的楼号和房间号-->", item[0], item[1])  # 1 101
            print("当前的session-->", session_value)
            power_value = before_power(item[0], item[1], session_value)
            if power_value != "其它情况":
                print("\033[92m获取到电量值{}度，宿舍楼{}号楼{}\033[0m".format(power_value, item[0], item[1]))
                # insert(item[0], item[1], power_value, db, cursor)
            else:
                print("获取电量值出现了其它情况")
                continue
        except Exception as e:
            warnings.warn("妈的出问题了，赶紧检查一下", UserWarning)
            print("异常信息如下\n", e)
            pass
        finally:
            print("——————————————————————这是分隔符—————————————————————")

    # 关闭数据库连接
    close_connect(db, cursor)
    # 结束时间
    end_time = time.time()
    print("总共耗时{}秒".format(end_time - start_time))
    # 总耗时时分秒
    m, s = divmod(end_time - start_time, 60)
    h, m = divmod(m, 60)
    print("总共耗时%02d时%02d分%02d秒" % (h, m, s))


if __name__ == '__main__':
    main()
