import pymysql

# 数据库连接
db = pymysql.connect(host='localhost',
                     port=3306,
                     user='root',
                     password='mysql',
                     database='xxt')

cursor = db.cursor()  # 获取游标
# 插入一条数据
SQL_INSERT_A_ITEM = "INSERT INTO xxt_table VALUES(1,2,3,4,5,6,7,8);"


def insert_a_item():
    try:
        cursor.execute(SQL_INSERT_A_ITEM)
        db.commit()
    except Exception as e:
        print('插入数据失败')
        print(e)
        db.rollback()


insert_a_item()
