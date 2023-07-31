# 计算哪个时间段的空闲机位最少
import pymysql


def time_window_iter(iter):
    window = []
    # 阈值时间
    threshold = 3600
    for x in iter:
        # print(x)
        window.append(x)
        while window and (x['datetime'] - window[0]['datetime']).total_seconds()>threshold:
            window.pop(0)
        # 如果窗口中的数据大于等于31条，就返回
        if len(window) >= threshold/60+1:
            yield window








def creatConnect():
    db = pymysql.connect(host='58.87.95.28', user='xjy_database', password='F46YPJA8MH7PcKYE', charset='utf8',
                         db='xjy_database')
    cursor = db.cursor()
    return db, cursor


def query(cursor):

    # sql = f"SELECT id, free, total, name,  datetime FROM bathroom_people WHERE name = '华科中区男浴室' AND DATE(datetime) = DATE (NOW());"
    sql = f"SELECT id, free, total, name,  datetime FROM bathroom_people WHERE name = '华科中区男浴室' AND DATE(datetime) = DATE(DATE_SUB(NOW(), INTERVAL 1 DAY));"

    cursor.execute(sql)
    results = []
    columns = [column[0] for column in cursor.description]  # 获取查询结果的列名
    for row in cursor.fetchall():
        result_dict = {}
        for i, value in enumerate(row):
            result_dict[columns[i]] = value
        results.append(result_dict)
    return results


def closeConnect(db, cursor):
    cursor.close()
    db.close()


if __name__ == '__main__':
    db, cursor = creatConnect()
    results = query(cursor)
    # for result in results:
    #     print(result)
    closeConnect(db, cursor)
    i=1
    for window in time_window_iter(results):
        i+=1
        print("第",i,"个时间段")
        # print(window)
        # 窗口的第一个时间
        print("开始时间"+str(window[0]['datetime']))
        # 窗口的最后一个时间
        print("结束时间"+str(window[-1]['datetime']))
        # 窗口的第一个时间和最后一个时间的差值
        print("时间段相差"+str((window[-1]['datetime']-window[0]['datetime']).total_seconds())+"秒")
        # 计算窗口中的free字段的平均值
        print("这段时间平均有"+str(103-sum([x['free'] for x in window])/len(window))+ "人在洗澡")
        print("------------------")
    # 求出哪个窗口的free字段的平均值最小
    # 用一个变量保存最小值
    min_avg = 0
    # 用一个变量保存哪个窗口的free字段的平均值最小
    min_window = []
    for window in time_window_iter(results):
        avg = sum([x['free'] for x in window])/len(window)
        if min_avg == 0 or avg < min_avg:
            min_avg = avg
            # min_window = list(window)
            min_window = window.copy()
    # 打印最小窗口的时间段
    print("洗澡人数最多的时间段"+str(min_window[0]['datetime'])+"到"+str(min_window[-1]['datetime']))
    print("平均有"+str(103-min_avg)+"人在洗澡")