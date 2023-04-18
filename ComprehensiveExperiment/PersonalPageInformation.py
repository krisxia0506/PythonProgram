"""
    获取老师个人页面的信息
"""
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re


# 获取页面内容
def getPersonalUrlContent(url):
    with urlopen(url) as fp:
        html = fp.read().decode()
    return html


# 根据页面内容提取信息
def getPersonalPageInformation(content):
    # 使用BeautifulSoup解析页面
    soup = BeautifulSoup(content, 'html.parser')

    # 提取页面中的纯文本
    text = soup.get_text().replace(' ', '').replace(' ', '')

    # 输出纯文本
    print(text)
    # 正则表达式

    # patter = r'姓名\n(.*?)\n'
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
    for key in patter:
        findall = re.findall(patter[key], text)
        # print("findall:", findall)
        if findall:
            init_data[key] = findall[0]
        else:
            init_data[key] = ''
    return init_data


if __name__ == '__main__':
    url = "https://cstd.ncist.edu.cn/szdw/syzxs/fd596c0697ed4d8fa3e7e70c61efe96b.htm"
    html = getPersonalUrlContent(url)
    information = getPersonalPageInformation(html)
    print(information)
