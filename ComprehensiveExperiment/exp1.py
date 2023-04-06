import re
import os
import os.path
from time import sleep
from urllib.parse import urljoin
from urllib.request import urlopen
from multiprocessing import Pool

dstDir = 'YuanShi'
if not os.path.isdir(dstDir):
    os.mkdir(dstDir)

url = r'http://www.cae.cn/cae/html/main/col48/column_48_1.html'
with urlopen(url) as fp:
    content = fp.read().decode()
pattern = r'<li class="name_list"><a href="(.+?)" target="_blank">(.+?)</a></li>'
result = re.findall(pattern, content)


def crawlEveryUrl(item):
    perUrl, name = item
    perUrl = urljoin(url, perUrl)
    name = os.path.join(dstDir, name)
    print(perUrl)
    try:
        with urlopen(perUrl) as fp:
            content = fp.read().decode()
    except:
        print('出错了一秒钟后自动重试…')
        sleep(1)
        crawlEveryUrl(item)
        return
    pattern = r'<img src="(.+?)" style=.*?/>'
    imgUrls = re.findall(pattern, content)
    if imgUrls:
        imgUrl = urljoin(url, imgUrls[0])
        try:
            with urlopen(imgUrl) as fpl:
                with open(name + '.jpg', 'wb') as fp2:
                    fp2.write(fpl.read())
        except:
            pass
    pattern = r'<p>(.+?)</p>'
    intro = re.findall(pattern, content, re.M)
    if intro:
        intro = '\n'.join(intro)
        intro = re.sub('(&ensp;)|(&nbsp;)|(<a href.*?</a>)', '', intro)
        with open(name + '.txt', 'w', encoding='utf8') as fp:
            fp.write(intro)


if __name__ == '__main__':
    with Pool(10) as p:
        p.map(crawlEveryUrl, result)
