from datetime import datetime, time
from time import sleep

import pymysql
import requests
def lib_request():
    while 1:
        url = 'http://apollo.ncist.edu.cn:90/default/Cur'
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
        # 获取当前时间
        current_time = datetime.now()

        # 格式化输出
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

        # 打印结果
        try:
            res = requests.get(url)
            print("当前时间"+ formatted_time+"目前在馆人数："+res.text)
            save_data(res.text)
        except Exception as e:
            print(e)
            pass
        finally:
            # 获取当前时间
            current_time = datetime.now().time()

            # 指定时间为22:30
            specified_time = time(22, 15)
            if current_time > specified_time:
                return # 结束程序
            # 休眠1分钟
            sleep(60)


# 将数据存在数据库中
def save_data(people_num):
    # 数据库连接
    db = pymysql.connect(host='58.87.95.28',
                         port=3306,
                         user='xjy_database',
                         password='F46YPJA8MH7PcKYE',
                         database='xjy_database')

    cursor = db.cursor()  # 获取游标
    # 插入一条数据
    SQL_INSERT_A_ITEM = f"INSERT INTO lib_people_num VALUES(null,{people_num},now());"

    def insert_a_item():
        try:
            cursor.execute(SQL_INSERT_A_ITEM)
            # print(SQL_INSERT_A_ITEM)
            db.commit()
        except Exception as e:
            print('插入数据失败')
            print(e)
            db.rollback()

    insert_a_item()

if __name__ == '__main__':
    lib_request()