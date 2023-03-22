import requests
import re
import os


def save_html(url):
    '''
    url:对应视频的url链接
    保存对应视频的html源码文件
    '''
    res = requests.get(url)
    res.encoding = "utf-8"
    name = url.split('/')[-1]
    with open(f"{name}.html", "w", encoding='utf-8') as fp:
        fp.write(res.text)


def handel_data(file, start=1, end=-1):
    '''
    file: html文件
    start: 选集起始 默认为第1集
    end: 选集结束 默认为最后1集
    '''
    with open("{}".format(file), "r", encoding="utf-8") as fp:
        data = fp.read()
    # 得到播放列表所有选集信息
    pageList = re.findall(
        r"<script>window.__INITIAL_STATE__=(.*?)</script>", data, re.MULTILINE)

    # 得到page part duration 对应选集集数 选集名字 选集时长(second)
    pages = re.findall(
        r'{"cid":.*?,"page":(.*?),"from":"vupload","part":(.*?),"duration":(\d*),"vid":.*?,"weblink":.*?,"dimension":.*?}',
        pageList[0])
    if end == -1:
        total_seconds = sum(int(page[-1]) for page in pages[start - 1:])
    else:
        total_seconds = sum(int(page[-1]) for page in pages[start - 1:end])
    hour = int(total_seconds / 60 / 60)
    minute = int((total_seconds - hour * 60 * 60) / 60)
    second = total_seconds - hour * 60 * 60 - minute * 60
    print('选集总时长为:{:02d}:{:02d}:{:02d}'.format(hour, minute, second))


def main():
    while True:
        # bv = input("请输入视频BV号: ")
        bv = "BV1Ya411S7aT" # ssm
        # bv = "BV1tL411c7gi"  # 软考
        while True:
            try:
                start = int(input("输入视频起始集: "))
            except ValueError:
                print("需要输入一个整数")
                continue
            else:
                break

        end = input("输入视频结束集(默认最后一集): ")
        url = 'https://www.bilibili.com/video/' + bv
        file_name = url.split('/')[-1] + '.html'
        try:
            if not os.path.exists(file_name):
                save_html(url)
            if end == '':
                handel_data(file_name, start)
            else:
                handel_data(file_name, start, int(end))
        except Exception as e:
            print("解析出错", e)
        while True:
            isContinue = input("是否继续？(y/n): ").lower()
            if isContinue not in ['y', 'n']:
                print("请输入正确选项(y/n)")
                continue
            if isContinue == 'n':
                print("Bye~")
                return
            break


if __name__ == "__main__":
    main()
