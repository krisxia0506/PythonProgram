import requests


def power(build, room, newsession):
    if build ==10 and room==636:
        room=635
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
    if r.text == 'RspBaseVO [code=ERROR, msg=系统繁忙，请稍后重试]':
        return 'sessionError'
    elif r.json()['returncode'] == '100':
        return r.json()['quantity']
    elif r.json()['returncode'] == 'FAIL':
        return 'noRoom'
    else:
        return 'otherError'
if __name__ == '__main__':
    print(power(10,636,"fc135a98-6b99-4ce4-b0ba-cb21a5cca7db"))