"""
    数据库操作
"""
import pymysql

class Mysql:
    def __init__(self,host,username,password,database):
        self.host = host
        self.username = username
        self.password = password
        self.database = database

    def saveToDB(self,init_data):
        host = self.host
        username = self.username
        password = self.password
        database = self.database
        # 连接到数据库
        conn = pymysql.connect(host=host, user=username, password=password, database=database)
        # 创建游标
        cursor = conn.cursor()
        # 检查数据库中是否存在与字典中的'name'键匹配的行
        sql = "SELECT * FROM t_teacher WHERE name = %s"
        cursor.execute(sql, (init_data.get('name')))
        # 获取查询结果 返回单个的元组，也就是一条记录(row)，如果没有结果 , 则返回 None
        row = cursor.fetchone()
        if row:
            # 如果存在，则更新该行的其他信息
            # 每个元素的格式为 "key=%s"，其中 key 是键名，%s 是占位符，用于在 SQL 查询语句中插入变量的值。
            # 例如，如果字典中有两个键，那么 columns 的值为 ["key1=%s", "key2=%s"]。
            columns = [key + "=%s" for key in init_data.keys() if key != 'name']
            sql = "UPDATE t_teacher SET {} WHERE name = %s".format(', '.join(columns))
            # UPDATE t_teacher SET key1=%s, key2=%s WHERE name = %s
            # 使用元组作为参数，其中元组的最后一个元素是 name 的值，其他元素是字典中除了 name 以外的键对应的值。
            # 因为元组是不可变的，所以它更加安全和可靠，能够有效地保护数据库免受 SQL 注入等安全攻击。
            cursor.execute(sql, tuple(
                [init_data.get(key) for key in init_data.keys() if key != 'name'] + [init_data.get('name')]))
            print(init_data.get('name') +'更新成功！')
        else:
            # 如果不存在，则插入新行
            columns = ', '.join(init_data.keys())
            values = ', '.join(['%s'] * len(init_data))
            sql = "INSERT INTO t_teacher ({}) VALUES ({})".format(columns, values)
            # INSERT INTO t_teacher (key1, key2) VALUES (%s, %s)
            cursor.execute(sql, tuple(init_data.values()))
            print(init_data.get('name') +'插入成功！')
        conn.commit()
        cursor.close()
        conn.close()

if __name__ == '__main__':
    init_data = {'name': '曾卉1', 'title': '高工32', 'degree': '学士', 'research_interests': '计算机应用',
                 'department': '计算机实验中心', 'email': 'zenghui@ncist.edu.cn',
                 'education': '河北工程大学本科，工学学士，1985', 'bio': ''}
    Mysql.saveToDB(init_data)
