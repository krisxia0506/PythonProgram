import requests

url = 'http://seat.ncist.edu.cn/libseat-ibeacon/saveBook'

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 12; PFTM10 Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.114 Safari/537.36 MMWEBID/9331 MicroMessenger/8.0.35.2360(0x2800235D) WeChat/arm64 Weixin Android Tablet NetType/WIFI Language/zh_CN ABI/arm64',
    'X-Requested-With': 'XMLHttpRequest',
    'Cookie': 'JSESSIONID=8D5FC018A3C7CF30AA1542B1BDC0E0F0;',
    'Host': 'seat.ncist.edu.cn',
    'Connection': 'close',
    'Accept': '*/*',
    'Referer': 'http://seat.ncist.edu.cn/libseat-ibeacon/seatdetail?linkSign=activitySeat&roomId=24&date=2023-07-06&buildId=1',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
}

params = {
    'seatId': '5435',
    'date': '2023-07-06',
    'start': '450',
    'end': '452',
    'type': '1',
    'captchaToken': ''
}

response = requests.get(url, headers=headers, params=params)

print(response.status_code)
print(response.text)
