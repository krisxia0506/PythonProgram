# 完整版
import pymysql
import requests


def getNewSession():
    url2 = 'http://h5cloud.17wanxiao.com:8080/CloudPayment/user/pay.do?versioncode=10556102&systemType=IOS&UAinfo=wanxiao&token=5c64d886-efb9-43ab-81f8-037276978059&customerId=104'
    res = requests.get(url2, allow_redirects=False)
    session = res.cookies.get("SESSION")
    return session


def power(build, room, newsession):
    if build == 10 and room == 636:
        room = 635
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
        "Cookie": f'SESSION={newsession}; SERVERID=e8e02aa88506006460462b373a5d91a9|1653700198|1653700055'
    }

    r = requests.post(url, headers=header)
    print(r.text)
    try:
        if r.text == 'RspBaseVO [code=ERROR, msg=系统繁忙，请稍后重试, subCode=null, subMsg=null]':
            return 'sessionError'
        elif r.json()['returncode'] == '100':
            return r.json()['quantity']
        elif r.json()['returncode'] == 'FAIL':
            return 'noRoom'
        else:
            return 'otherError'
    except:
        return 'otherError'


def creatConnect():
    db = pymysql.connect(host='101.200.229.85', user='root', password='1c0K@U*Y1E3-n', charset='utf8', db='ACEQIS')
    cursor = db.cursor()
    return db, cursor


def insert(buildID, roomID, power, db, cursor):
    sql = f"INSERT INTO PowerTable (buildID,roomID,power,date) VALUES ({buildID},{roomID},{power},date_sub(CURDATE()-1,interval 1 minute ))"
    cursor.execute(sql)
    db.commit()


def closeConnect(db, cursor):
    cursor.close()
    db.close()


def quey(roomID, session2):
    flag = power(building, room, session2)
    if flag == 'sessionError':
        return flag
    elif flag == 'otherError':
        quey(roomID, session2)
    elif flag == 'noRoom':
        return flag
    else:
        print(building, room, flag)
        insert(building, room, flag, db, cursor)
        return 1


if __name__ == '__main__':
    session1 = ""
    db, cursor = creatConnect()

    for bu in range(1, 12):

        building = bu
        if building == 8:
            start = 1
            end = 20
            for i in range(1, 5):  # ABCD区
                i = i * 1000
                for j in range(1, 7):  # 1-6楼
                    j = j * 100
                    a = i + j + start  # 1101
                    b = i + j + end  # 1120
                    for room in range(a, b + 1):
                        while quey(room, session1) == "sessionError":
                            session1 = getNewSession()
        else:
            start = 1
            end = 70
            for i in range(1, 7):
                i = i * 100
                a = i + start
                b = i + end
                for room in range(a, b + 1):
                    print(session1)
                    while quey(room, session1) == "sessionError":
                        session1 = getNewSession()

    closeConnect(db, cursor)
