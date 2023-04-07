"""
    该项目的目的是爬取网页中的所有老师的个人信息
    包括：照片、姓名、职称、学位、研究方向、所在系教研室、邮箱、教育背景、个人简介
    使用的技术：正则表达式、BeautifulSoup、多进程、数据库操作、文件操作、异常处理、面向对象编程、多python文件编程
    1.爬取网页中的所有老师姓名和个人页面的url，作为元组存储在列表中
    2.为每个老师创建文件夹
    3.爬取每个老师的个人页面的照片和个人信息
"""
from __future__ import unicode_literals

import os
import re
from time import sleep
from urllib.parse import urljoin
from urllib.request import urlopen
from multiprocessing import Pool

from bs4 import BeautifulSoup

from ComprehensiveExperiment.testMysql import Mysql

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
def createPersonalFolder(result):
    current_path = os.getcwd()
    ncist_folder_path = 'NCIST'
    if not os.path.isdir(ncist_folder_path):
        os.mkdir(ncist_folder_path)
    # 创建每个人的文件夹
    for i in result:
        name = i[1]
        # 判断NCIST文件夹下是否有name文件夹
        # 如果没有就创建
        everyone_folder_path = os.path.join(current_path, ncist_folder_path, name)
        if not os.path.isdir(everyone_folder_path):
            os.mkdir(everyone_folder_path)


# 爬取每个老师的个人页面
def crawlEveryUrl(item):
    personalPageUrl, name = item
    personalPageUrl = urljoin(url, personalPageUrl)
    print(name + "的个人页面：" + personalPageUrl)
    crawlPicture(personalPageUrl, name)
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
        return
    # 正则表达式匹配图片
    img_pattern = r'<img[^>]*src="(/pub/jsjxy/images/[^"]+\.jpg)"[^>]*>'
    imgUrls = re.findall(img_pattern, content)
    if imgUrls:
        imgUrl = urljoin(url, imgUrls[0])
        print(imgUrls)
        try:
            with urlopen(imgUrl) as fpl:
                with open(name_folder + '.jpg', 'wb') as fp2:
                    fp2.write(fpl.read())
        except:
            pass
    else:
        print(name + "没有图片")


# 对个人页面进行信息提取
def personalPageInformation(personalPageUrl):
    # 获取页面内容
    with urlopen(personalPageUrl) as fp:
        html = fp.read().decode()

    # 使用BeautifulSoup解析页面
    soup = BeautifulSoup(html, 'html.parser')

    # 提取页面中的纯文本
    text = soup.get_text() \
        .replace(' ', '') \
        .replace(' ', '')

    # 输出纯文本
    # print(text)
    # 正则表达式字典
    patter = {
        'name': r'姓名\n(.*?)\n\n',
        'title': r'职称\n(.*?)\n\n',
        'degree': r'学位\n(.*?)\n\n',
        'research_interests': r'研究方向\n(.*?)\n\n',
        'department': r'所在系教研室\n(.*?)\n\n',
        'email': r'邮箱\n(.*?)\n\n',
        'education': r'教育背景\n(.*?)\n\n',
        'bio': r'个人简介\n(.*?)\n\n',
    }
    # 初始化字典
    init_data = {
        'name': '',
        'title': '',
        'degree': '',
        'research_interests': '',
        'department': '',
        'email': '',
        'education': '',
        'bio': ''
    }
    # 正则表达式匹配
    for key in patter:
        findall = re.findall(patter[key], text)
        if findall:
            init_data[key] = findall[0]
        else:
            init_data[key] = ''
    print(init_data)
    saveToDB(init_data)


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
