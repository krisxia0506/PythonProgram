import os
import re
from time import sleep
from urllib.parse import urljoin
from urllib.request import urlopen


def img_download(item, folder_path=''):
    print("正在下载藏品 " + item[1] + " 的图片…1%")
    detail_url = "https://digicol.dpm.org.cn/cultural/detail?id=" + item[0]
    # print("藏品 " + item[1] + "的详情url-->" + detail_url)
    name_folder = os.path.join(folder_path, item[2] + "_" + item[1])
    # print("藏品 " + item[1] + "的文件夹-->" + name_folder)
    try:
        # 打开详情页面
        with urlopen(detail_url) as fp:
            detail_content = fp.read().decode()
    except:
        print('出错了一秒钟后自动重试…')
        sleep(1)
        img_download(item, folder_path)
        return
    img_iframe_pattern = r'''<iframe id="image_iframe_id" src="(.+?)" width="100%" height="100%" scrolling="no" marginheight="0" marginwidth="0" style="border:none;"></iframe>'''
    findall = re.findall(img_iframe_pattern, detail_content)
    img_iframe = urljoin("https://digicol.dpm.org.cn/", findall[0])
    # print("藏品图片的iframe地址-->" + img_iframe)
    print("正在下载藏品 " + item[1] + " 的图片…50%")
    try:
        with urlopen(img_iframe) as fp:
            img_iframe_content = fp.read().decode()
    except:
        print('出错了一秒钟后自动重试…')
        sleep(1)
        img_download(item, folder_path)
        return
    img_pattern = r'''<div class="swiper-slide" data-id="0"> <img src="(.+?)"> </div>'''
    img_findall = re.findall(img_pattern, img_iframe_content)
    # print("藏品图片url-->" + img_findall[0])
    if img_findall:
        # print(item[1] + "的照片url:" + str(img_findall))
        try:
            with urlopen(img_findall[0]) as fpl:
                with open(name_folder + '.png', 'wb') as fp2:
                    fp2.write(fpl.read())
                    print(item[1] + '  图片下载成功')
        except:
            pass


if __name__ == '__main__':
    items = ('707410e4ae914ed78ae9bde3ca778d26', '冷枚梧桐双兔图轴', '故00005183')
    img_download(items, '故宫')
