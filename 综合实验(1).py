import json
import os
import re
from urllib.parse import urljoin
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup

dstDir = 'gugong'
if not os.path.isdir(dstDir):
    os.mkdir(dstDir)


def POST():
    """
    模拟故宫文物绘画页面的请求，获取绘画文物信息
    :return: 文物列表，包含文物的uuid、文物的名字和文物号，以元组成对存储在列表中
    """
    url = "https://zm-digicol.dpm.org.cn/cultural/queryList"
    # post参数
    post_data = {
        'page': '1',
        'pageSize': '50',
        'keyWord': '',
        'cateList': '17',
        'sortType': '',
        'hasImage': 'false',
        'ranNum': '0.9093449507377198'
    }
    req = requests.post(url, data=post_data)  # post请求返回req对象

    # 如果请求返回的json数据，则可以用json的一个函数转换
    data = json.loads(req.text)  # 响应体内容是字符串，不便操作。把响应体格式化为json格式，便于解析
    print("\npost请求的响应体-->" + str(data))
    list = []
    # data['rows']列表中存放多个字典，每个字典中包含一个文物的信息
    for i in range(len(data['rows'])):
        # 获取每个文物的uuid
        uuid = data['rows'][i]['uuid']
        # 获取每个文物的name
        name = data['rows'][i]['name']
        # 获取文物号
        cultural = data['rows'][i]['culturalRelicNo']
        # 把所有文物的id,name,文物号存放在列表中，每个文物的id,name，文物号存放在一个元组中,追加到列表中
        list.append((uuid, name, cultural))
    print("\n所有文物列表-->", list)
    return list


def GET(item):
    """
        获取作品的详细介绍
        :param item:元组，包含uuid，name，文物号
        :return 字符串，详细介绍
    """
    url = "https://www.dpm.org.cn/searchs/paints.html?0.39148352645548523&category_id=91&times=&types=&sort=sortrank&new_authors=&names=" + \
          item[1] + "&dbg=0"
    # get请求返回req对象
    req = requests.get(url)
    # print(req.text)
    # 利用正则表达式匹配进入文物介绍页的链接(相对地址)
    link_pattern = r'<a target="_blank" href="(.*?)" id=".*">'
    link_result = re.findall(link_pattern, req.text)[0]
    # 拼接进入文物详情页的链接（绝对地址）
    perurl = urljoin('https://www.dpm.org.cn/', link_result)
    # print(perurl)
    try:
        with urlopen(perurl) as fp:
            content = fp.read().decode()
    except:
        pass
    # print(content)
    # 匹配文物详情页的介绍部分
    p_pattern = r'<p>(.*?)</p>'
    # re.DOTALL让正则表达式中的"."可以匹配到换行符，实现跨行匹配
    p_result = re.findall(p_pattern, content, re.DOTALL)[0]
    # 匹配标签中可能存在的tag提示
    tag_pattern = r'TAG标签耗时：.+?秒'
    # 用空字符替换掉tag提示（删除tag提示）
    p_result = re.sub(tag_pattern, '', p_result)
    # print(p_result)
    #  BeautifulSoup对象 = BeautifulSoup（要解析的文本,'解析器'）
    # html.parser 是python内置的标准库，解析快
    soup = BeautifulSoup(p_result, 'html.parser')
    introduce = soup.get_text()
    # print(introduce)
    # introduce = introduce.replace(' ', '').replace('　', '')
    # print(introduce)
    return introduce


# 获取文物基本信息,写入文件
def get_detail_information(item):
    """
    获取文物信息，并保存到同名的txt文件中
    :param item: 元组，包含uuid，name，文物号
    :return: 无返回值
    """
    print("\n开始保存" + item[1] + "的基本信息")
    # 文物名称是超链接(由固定部分和uuid组成)
    detail_url = 'https://digicol.dpm.org.cn/cultural/detail?id=' + item[0]
    with urlopen(detail_url) as fp:
        content = fp.read().decode()
        fp.close()
    # print(content)
    # ----利用正则表达式获取文物信息----
    # 提取文物名称的正则表达式
    name_pattern = r'<h2>(.*?)</h2>'
    # 提取文物号
    numbers_pattern = r'<li><span>Number</span><font>(.*?)</font></li>'
    # 提取分类
    category_pattern = r'<li><span>Category</span><font>(.*?)</font></li>'
    # 提取年代
    period_pattern = r'<li><span>Period</span><font>(.*?)</font></li>'
    # findall查找出所有匹配项，返回一个列表，但仅需列表中的第一项
    name_result = re.findall(name_pattern, content)[0]
    numbers_result = re.findall(numbers_pattern, content)[0]
    category_result = re.findall(category_pattern, content)[0]
    period_result = re.findall(period_pattern, content)[0]
    print("文物名：" + name_result)
    print("文物号：" + numbers_result)
    print("文物分类：" + category_result)
    print("文物年代：" + period_result)
    # 创建以item[2] + item[1]为名的txt文件，将文物信息内容写入
    # 路径
    folder = os.path.join("gugong", item[1], item[2] + item[1])
    # 操作系统的路径中不能存在/所以将其替换成-
    folder = re.sub(r'/', '-', folder)
    # print(folder)
    with open(folder + '.txt', 'w', encoding='utf8') as fp:
        # 调用GET函数获取文物介绍
        introduce = GET(item)
        txt = '文物名称:' + name_result + '\n文物号:' + numbers_result + '\n分类:' + category_result + '\n年代:' + period_result + '\n介绍：' + introduce
        print("\n保存的文物信息如下:\n" + txt)
        fp.write(txt)
        fp.close()
        print("\n文物信息保存成功")


# 获取文物图片
def get_img(item):
    print("\n开始下载"+item[1]+"的图片")
    # 文物信息页面
    detail_url = 'https://digicol.dpm.org.cn/cultural/detail?id=' + item[0]
    with urlopen(detail_url) as fp:
        content = fp.read().decode()
        # print(content)
    # 利用正则表达式获取文物图片的相对地址
    # 图片并非以img标签存放于文物信息页面中，而是通过文物信息页面中的iframe标签展示，图片在iframe指向的网页中
    # 通过iframe里的超链接进入图片页面，图片页面的img标签存放文物图片
    iframe_pattern = r'<iframe id="image_iframe_id" src="(.*?)" width="100%" height="100%" scrolling="no"'
    iframe_url = re.findall(iframe_pattern, content)[0]
    iframe_url = 'https://digicol.dpm.org.cn' + iframe_url
    print("\n成功提取出iframe页面-->" + iframe_url)
    # 在文物图片网页获取文物图
    with urlopen(iframe_url) as fp:
        iframe_content = fp.read().decode()
        # print(iframe_content)
    img_pattern = r'<div class="swiper-slide" data-id="0"> <img src="(.*?)"> </div>'
    img_url = re.findall(img_pattern, iframe_content)[0]
    print("\n成功提取出图片的url-->" + img_url)
    # 路径
    folder = os.path.join("gugong", item[1], item[2] + item[1])
    # 路径中不能存在/所以将其替换成-
    folder = re.sub(r'/', '-', folder)
    if img_url:
        try:
            with urlopen(img_url) as fp1:
                with open(folder + '.jpg', 'wb') as fp2:
                    fp2.write(fp1.read())
                    fp2.close()
                    print("\n下载图片成功")
        except:
            print("\n下载图片失败")
            pass


# 每个文物的id,name存放在一个元组中，所有文物的id,name存放在列表中，
all_list = POST()
count = len(all_list)
now = 1
# 遍历每个文物，item存放每个文物的id,name
for item in all_list:
    print("正在爬取第" + str(now) + "个文物" + "共" + str(count) + "个文物")
    # 为每个文物创建文件夹
    dstDir = 'gugong\\' + item[1]
    if not os.path.isdir(dstDir):
        os.mkdir(dstDir)
    # 获取文物信息并存储在文件中
    get_detail_information(item)
    # 获取文物图片
    get_img(item)
    now = now + 1
