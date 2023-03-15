import requests

url = "https://cs-ol.sns.sohu.com/330008/v7/feeds/show?feed_id=1001536252866140928&flyer=1676431665810&appid=330008&app_key_vs=1.0.0&sig=3b2d816bd162645e3c233b1bd47959a2"
head = {
    'Content-type': 'application/json; charset=UTF-8',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Origin': 'https://docs.qq.com',

    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
}
url2="https://dm-ol.sns.sohu.com/openapi/tracking/api/v1/miniapp/events"
head2 = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh',
    'Connection': 'keep-alive',
    'Content-Length': '903',
    'Content-Type': 'application/json',
    'Host': 'dm-ol.sns.sohu.com',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'referer': 'https://servicewechat.com/wx915c6f684ab5b15f/159/page-frame.html',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF XWEB/6500',
    'xweb_xhr': '1'
}
data='{"request_id":"04a6445208e3b42756adca40b9fa83e6","events":[{"PublicMeta":{"platform":"weixin","miniId":"wx915c6f684ab5b15f","platform_uid":"o8c6v4sNwYo97A4_WsVV1GmZ_yFA","rela_hy_id":"o3fMFwkl6gbbCrf9EtVqLvvEAtMs","event":"E_PAGE_VIEW","event_detail":"FEED_DETAIL","createTime":1676432369133,"submitTime":1676432369133,"version":"1.3.1","properties":{"circleId":"917544916408806784","feedId":"1001536252866140928","circlePartition":"","sourceClick":"SC_OTHER"},"sessionId":"le53k2814eqsonarnth","cid":"x0110520101016898d3b96846000769675779cdf0e4c","uid":"942549459513063936","tel":"","token":"eyJleHAiOjE2ODM3OTkwMzQ4NTMsImlhdCI6MTY3NjAyMzAzNDg1MywicHAiOiIxNTY2NzAxNDAzMTEwNTgwMjI0QHNvaHUuY29tIiwidGsiOiJteFBXRks0UVUyTlNHM1pMczUxV3NPQUhDcUdUMXRheiIsInYiOjB9.TMmoGcT-MG7WpihtcxF7rbm9ldtkQjVk2Sbre0wZSEo"},"BasicMeta":{"system":"Windows 10 x64","model":"microsoft","brand":"microsoft","netType":"wifi"}}]}'
while 1:
    try:
        res = requests.get(url, headers=head)
        res2 = requests.post(url2, headers=head2,data=data)
        print("点击量:"+str(res.json()['data']['sourceFeed']['exposureCount']))
        print(res2.text)
    except:
        pass
