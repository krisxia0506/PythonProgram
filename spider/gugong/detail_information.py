import re
from time import sleep
from urllib.parse import urljoin
from urllib.request import urlopen

import requests
from bs4 import BeautifulSoup


# 获取藏品文物号，分类，年代
def get_detail_information(item):
    print("正在获取藏品 " + item[1] + " 的文物号，分类，年代…")
    detail_url = "https://digicol.dpm.org.cn/cultural/detail?id=" + item[0]
    # print("藏品 " + item[1] + "的详情url-->" + detail_url)
    try:
        # 打开详情页面
        with urlopen(detail_url) as fp:
            detail_content = fp.read().decode()
    except:
        print('出错了一秒钟后自动重试…')
        sleep(1)
        get_detail_information(item)
        return
    # print(detail_content)
    # 文物号正则
    number_pattern = r'''<li><span>Number</span><font>(.+?)</font></li>'''
    # 分类正则
    category_pattern = r'''<li><span>Category</span><font>(.+?)</font></li>'''
    # 年代正则
    period_pattern = r'''<li><span>Period</span><font>(.+?)</font></li>'''
    number = re.findall(number_pattern, detail_content)
    category = re.findall(category_pattern, detail_content)
    period = re.findall(period_pattern, detail_content)
    # print("藏品名-->" + item[1])
    # print("藏品文物号-->" + number[0])
    # print("藏品分类-->" + category[0])
    # print("藏品年代-->" + period[0])
    # 保存为字典
    detail_information = {
        'name': item[1],
        'id': number[0],
        'category': category[0],
        'period': period[0],
        'introduce': get_introduce(item)
    }
    return detail_information


# 获取藏品介绍，被get_detail_information调用
def get_introduce(item):
    search_url = f"https://www.dpm.org.cn/searchs/paints.html?0.19446695075223586&category_id=91&times=&types=&sort=sortrank&new_authors=&names={item[1]}&dbg=0"
    response = requests.get(search_url)
    # 正则表达式
    pattern = r'''<a target="_blank" href="(.+?)" id=".*?">.*?'''
    introduce_url = re.findall(pattern, response.text)[0]
    introduce_url = urljoin("https://www.dpm.org.cn/", introduce_url)
    # print(response.text)
    # print("藏品介绍url-->" + introduce_url)
    try:
        # 打开详情页面
        with urlopen(introduce_url) as fp:
            introduce_content = fp.read().decode()
    except:
        print('出错了一秒钟后自动重试…')
        sleep(1)
        get_introduce(item)
        return
    # print(introduce_content)
    # 介绍正则
    introduce_pattern = r'''<p>(.+?)<span style="display:none;">'''
    # re.DOTALL     它可以将.匹配符扩展到跨行，从而匹配包括换行符在内的任意字符。
    introduce_findall = re.findall(introduce_pattern, introduce_content, re.DOTALL)[0]
    # print(introduce_findall)
    # print("藏品介绍-->" + introduce_findall)
    soup = BeautifulSoup(introduce_findall, 'html.parser')
    introduce_text = soup.get_text().replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '').replace('　',
                                                                                                                    '')
    # print("藏品介绍-->" + introduce_text)
    return introduce_text


if __name__ == '__main__':
    items = ('707410e4ae914ed78ae9bde3ca778d26', '冷枚梧桐双兔图轴', '故00005183')
    get_detail_information(items)
    get_introduce(items)
