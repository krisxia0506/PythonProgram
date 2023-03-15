import requests

url = "https://docs.qq.com/cgi-bin/like/like?u=dfe656aaeafe4addb89f84632ea01172"
head = {
    'Content-type': 'application/x-www-form-urlencoded',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Host': 'docs.qq.com',
    'Origin': 'https://docs.qq.com',
    'Referer': 'https://docs.qq.com/sheet/DQWJWVHdsREZ0aldN?tab=BB08J2&u=dfe656aaeafe4addb89f84632ea01172',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0',
    'Cookie': 'pgv_pvid=1672234502250513; fingerprint=25b9775525114bb180258f1b793ec9c417; low_login_enable=1; RK=zcWxH8Tkv6; ptcz=ccffcf0209825b5ab62ecc8d08e93525e8cf18b05c6e5348d4cbcbb736d6e390; luin=o2547359996; lskey=00010000aaa6aec8f35b09d680e93d274d581f659f570dd2f1c4412f381dbb9aeb01cbb7aac56c1c6671e2bf; p_luin=o2547359996; p_lskey=000400005f6a58606656bdaa92725c8a59b25f336ffdf192c5ca34f7d442f354af17debbef74352eeccb04e9; DOC_SID=161b6e8223b74241ade3bdc724c86d732b031fae61bd4371be44e7580430f066; SID=161b6e8223b74241ade3bdc724c86d732b031fae61bd4371be44e7580430f066; loginTime=1672458383274; optimal_cdn_domain=docs2.gtimg.com; backup_cdn_domain=docs.gtimg.com; adtag=doc_list_rightclk_form; adtag=doc_list_rightclk_form; go_session_id=YWQyYTdjNTYtYWIzNy00MWI3LTk1YjEtZmQzYmM3Y2YwZmQz.98a61eb42e5ae3b73ade4037dd760357df706eb0; traceid=fad2d2056a; TOK=fad2d2056ace7300; hashkey=fad2d205'
}
data = {"file_id": "AbVTwlDFtjWM", "icon_id": "109"}
i =0
while 1:
    i=i+1
    res = requests.post(url, data=data, headers=head)
    print(i)
    print(res.text)
