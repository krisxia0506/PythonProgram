"""
    该项目的目的是爬取网页中的所有老师的个人信息
    包括：照片、姓名、职称、学位、研究方向、所在系教研室、邮箱、教育背景、个人简介
    使用的技术：正则表达式、BeautifulSoup、多进程、数据库操作、文件操作、异常处理、面向对象编程、多python文件编程
    1.爬取网页中的所有老师姓名和个人页面的url，作为元组存储在列表中
    2.为每个老师创建文件夹
    3.爬取每个老师的个人页面的照片和个人信息
"""

import os
import re
from time import sleep
from urllib.parse import urljoin
from urllib.request import urlopen
from multiprocessing import Pool


from PersonalPageInformation import getPersonalUrlContent, getPersonalPageInformation
from testMysql import Mysql

# 获取页面内容
url = r'https://cstd.ncist.edu.cn/szdw/index.htm'
with urlopen(url) as fp:
    content = fp.read()
    content = content.decode()

# 正则表达式
pattern = r'''<a href='(.+?)' .*?>(.+?)</a>'''
result = re.findall(pattern, content)
print("网页中匹配到的所有老师姓名" + str(result))


# 为每个老师创建文件夹
def createPersonalFolder(teacher_list):
    current_path = os.getcwd()
    ncist_folder_path = 'NCIST'
    if not os.path.isdir(ncist_folder_path):
        os.mkdir(ncist_folder_path)
    # 创建每个人的文件夹
    for i in teacher_list:
        name = i[1]
        # 判断NCIST文件夹下是否有name文件夹
        # 如果没有就创建
        everyone_folder_path = os.path.join(current_path, ncist_folder_path, name)
        if not os.path.isdir(everyone_folder_path):
            os.mkdir(everyone_folder_path)


# 爬取每个老师的个人页面，入口
def crawlEveryUrl(item):
    personalPageUrl, name = item
    personalPageUrl = urljoin(url, personalPageUrl)
    print(name + "的个人页面：" + personalPageUrl)
    # 抓取图片
    crawlPicture(personalPageUrl, name)
    # 抓取个人信息
    personalPageInformation(personalPageUrl)


# 爬取图片
def crawlPicture(personalPageUrl, name):
    name_folder = os.path.join("NCIST", name, name)
    try:
        # 打开个人页面
        with urlopen(personalPageUrl) as fp:
            content = fp.read().decode()
    except:
        print('出错了一秒钟后自动重试…')
        sleep(1)
        crawlPicture(personalPageUrl, name)
        return
    # 正则表达式匹配图片
    img_pattern1 = r'<img[^>]*src="(/pub/jsjxy/images/[^"]+\.jpg)"[^>]*>'
    img_pattern2 = r'<img[^>]*src="(/pub/jsjxy/images/[^"]+\.png)"[^>]*>'
    img_pattern3 = r'<img[^>]*src="(../../images/2022-04/[^"]+\.jpg)"[^>]*>'
    img_urls1 = re.findall(img_pattern1, content)
    img_urls2 = re.findall(img_pattern2, content)
    img_urls3 = re.findall(img_pattern3, content)
    if img_urls1:
        imgUrl = urljoin(url, img_urls1[0])
        print(name+"的个人照片url:"+str(img_urls1))
        try:
            with urlopen(imgUrl) as fpl:
                with open(name_folder + '.jpg', 'wb') as fp2:
                    fp2.write(fpl.read())
                    print(name+'图片下载成功')
        except:
            pass
    elif img_urls2:
        imgUrl = urljoin(url, img_urls2[0])
        print(name+"的个人照片url:"+str(img_urls2))
        try:
            with urlopen(imgUrl) as fpl:
                with open(name_folder + '.png', 'wb') as fp2:
                    fp2.write(fpl.read())
                    print(name + '图片下载成功')
        except:
            pass
    elif img_urls3:
        imgUrl = urljoin(url, img_urls3[0])
        print(name+"的个人照片url:"+str(img_urls3))
        try:
            with urlopen(imgUrl) as fpl:
                with open(name_folder + '.jpg', 'wb') as fp2:
                    fp2.write(fpl.read())
                    print(name + '图片下载成功')
        except:
            pass
    else:
        print(name + "没有图片")


# 对个人页面进行信息提取
# 多python文件编程
def personalPageInformation(personal_page_url):
    # 获取页面内容
    personal_page_content = getPersonalUrlContent(personal_page_url)
    information = getPersonalPageInformation(personal_page_content)
    print(information)
    saveToDB(information)


# 数据库操作,保存到数据库
# 面向对象
def saveToDB(init_data):
    mysql = Mysql(
        '127.0.0.1',
        'root',
        'mysql',
        'ncist'
    )
    mysql.saveToDB(init_data)


if __name__ == '__main__':
    # 创建文件夹
    createPersonalFolder(result)
    with Pool(10) as p:
        p.map(crawlEveryUrl, result)
