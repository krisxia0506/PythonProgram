import os

from post_index import post_request
from img_download import img_download
from detail_information import get_detail_information, get_introduce
from save_mysql import Mysql

folder_path = '故宫'
if not os.path.isdir(folder_path):
    os.mkdir(folder_path)

url = "https://zm-digicol.dpm.org.cn/cultural/queryList"
items_list = post_request(url)
print("所有藏品列表-->" + str(items_list))

if __name__ == '__main__':
    for item in items_list:
        img_download(item, folder_path)
        information = get_detail_information(item)
        get_introduce(item)
        print(information)
        mysql = Mysql('localhost', 'root', 'mysql', 'gugong')
        mysql.saveToDB(information)
