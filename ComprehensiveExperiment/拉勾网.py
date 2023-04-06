from selenium import webdriver
import time
import pymysql
from bs4 import BeautifulSoup

# 控制爬取页数
num = 1


# 初始化Selenium
def init():
    # 控制台输入想要查询的工作
    name = input("请输入工作:")

    driver = webdriver.Chrome()
    # 全屏
    driver.maximize_window()
    # 请求拉勾网首页
    driver.get("https://www.lagou.com/")
    # 参考图1，根据id关闭进入到首页的弹窗
    driver.find_element_by_id("cboxClose").click()
    time.sleep(1)

    # 参考图2，根据id控制输入框输入后点击搜索
    driver.find_element_by_id("search_input").send_keys(str(name))
    time.sleep(0.5)
    driver.find_element_by_id("search_button").click()
    time.sleep(1)

    # 参考图3，关闭搜索后出现的广告
    driver.find_element_by_class_name("body-btn").click()

    # 获取搜索后得到的网页代码并返回
    source = driver.page_source
    return source, driver


# 初始化mysql
def init_mysql():
    dbparams = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': '数据库账号',
        'password': '数据库密码',
        'database': 'lagou',
        'charset': 'utf8'
    }
    # 初始化数据库连接
    conn = pymysql.connect(**dbparams)
    cur = conn.cursor()
    return cur, conn


# 数据爬取
def index(cur, source, driver):
    # 引用全局变量num
    global num

    # 数据库插入语句
    sql = "insert into lagou(id,title, company, price, experience, education, text, address) values(null,%s,%s,%s,%s,%s,%s,%s)"

    # 使用BeautifulSoup解析
    bs = BeautifulSoup(source, "lxml")

    # 参考图4，拿到所有li标签然后遍历
    li_list = bs.find_all(class_="con_list_item default_list")
    for li in li_list:
        bs = BeautifulSoup(str(li), "lxml")

        # 参考图5，根据li标签中的属性拿值
        # 职位名称
        title = bs.find("li")["data-positionname"]
        # 公司名称
        company = bs.find("li")["data-company"]
        # 详情页url
        url = bs.find(class_="position_link")["href"]

        # 请求详情页，进行数据爬取
        driver.get(url)
        page_source = driver.page_source
        page_bs = BeautifulSoup(page_source, "lxml")

        # 参考图6，获取所有文本值，strip()首尾去除空格
        data = page_bs.find(class_="job_request").text.strip()
        # 根据 / 分割拿值
        # 薪资范围，有的薪资后有些用 · 拼接多余的，我们分割取值
        price = data.split("/")[0].strip().split("·")[0]
        # 经验要求
        experience = data.split("/")[2].strip()
        # 学历
        education = data.split("/")[3].strip()

        # 职位描述，参考图7
        text = page_bs.find(class_="job-detail").text.strip()

        # 参考图8，替换多余的"查看地图"，根据"-"分割然后遍历拼接起来，以达到去除中间空格的目的
        address = page_bs.find(class_="work_addr").text.strip().replace(" ", "").replace("查看地图", "").split("-")
        addr = ""
        for addre in address:
            addr += addre + "-"

        # 工作地址
        addr = addr.rstrip("-")

        # 执行SQL
        cur.execute(sql, (title, company, price, experience, education, text, addr))
        # 提交事务
        conn.commit()

    # 由于爬取完一页后浏览器会停留在最后一条数据的详情页，则我们需要返回到搜寻工作后的页面进行翻页
    # 每页有14条数据，控制浏览器返回14次
    for i in range(14):
        driver.back()

    # 控制num大小进行多页爬取
    if num <= 3:
        # print(num)
        num += 1
        # 实践测试，多睡眠一些时间，防止被拦截
        time.sleep(5)
        # 点击下一页，参考图9
        driver.find_element_by_class_name("pager_next").click()
        time.sleep(0.5)
        next_source = driver.page_source
        # 再次进行数据爬取
        index(cur, next_source, driver)


# 关闭数据库连接
def close(cur, conn):
    cur.close()
    conn.close()


# 开始
if __name__ == "__main__":
    source, driver = init()

    # python可以返回并接受多个值，用逗号分隔
    cur, conn = init_mysql()

    # 数据爬取
    index(cur, source, driver)
    # 关闭
    close(cur, conn)
