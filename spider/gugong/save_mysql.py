import pymysql


class Mysql:
    def __init__(self, host, username, password, database):
        self.host = host
        self.username = username
        self.password = password
        self.database = database

    def saveToDB(self, init_data):
        host = self.host
        username = self.username
        password = self.password
        database = self.database
        # 连接到数据库
        conn = pymysql.connect(host=host, user=username, password=password, database=database)
        # 创建游标
        cursor = conn.cursor()
        # 检查数据库中是否存在与字典中的'id'键匹配的行
        sql = "SELECT * FROM t_object WHERE id = %s"
        cursor.execute(sql, (init_data.get('id'),))
        row = cursor.fetchone()
        if row:
            # 如果存在，则更新该行的其他信息
            # 每个元素的格式为 "key=%s"，其中 key 是键名，%s 是占位符，用于在 SQL 查询语句中插入变量的值。
            columns = [key + "=%s" for key in init_data.keys() if key != 'id']
            sql = "UPDATE t_object SET {} WHERE name = %s".format(', '.join(columns))
            # 使用元组作为参数，其中元组的最后一个元素是 name 的值，其他元素是字典中除了 name 以外的键对应的值。
            # 因为元组是不可变的，所以它更加安全和可靠，能够有效地保护数据库免受 SQL 注入等安全攻击。
            cursor.execute(sql, tuple(
                [init_data.get(key) for key in init_data.keys() if key != 'id'] + [init_data.get('id')]))
            print(init_data.get('name') + '更新数据库成功！')
        else:
            # 如果不存在，则插入新行
            columns = ', '.join(init_data.keys())
            values = ', '.join(['%s'] * len(init_data))
            sql = "INSERT INTO t_object ({}) VALUES ({})".format(columns, values)
            cursor.execute(sql, tuple(init_data.values()))
            print(init_data.get('name') + '插入数据库成功！')
        conn.commit()
        cursor.close()
        conn.close()


if __name__ == '__main__':
    init_data = {'name': '冷枚梧桐双兔图轴', 'id': '故00005183', 'category': 'Paintings', 'period': '清',
                 'introduce': '《梧桐双兔图》轴，清，冷枚绘，绢本，设色，纵176.2厘米，横95厘米。本幅款署“臣冷枚恭画”，钤“臣”朱文印，“冷枚”、“夙夜匪解”白文印二方。此图似为中秋佳节而作。图中野菊满地，桂花飘香，高大的梧桐树下，两只肥硕的白兔惬意地在草地上嬉戏。双兔写实，造型准确生动，皮毛以细笔一一画出，具有柔软的质感。兔目用白色点出高光，令眼神活灵活现顿生神采。山石以折带笔方正写出，于坚硬中见峻峭之美。构图疏密有致，设色注重冷暖色调的对比。整幅作品大气秀美，富丽堂皇，受到了西洋绘画技法的影响，具有康熙朝宫廷绘画的风貌。冷枚（约1670—1742年），清初宫廷画家，字吉臣，别号金门画史，胶州（今属山东省）人。师从清初宫廷画家焦秉贞，擅长画人物、仕女、山水、花鸟，画风工整细致，色彩浓厚。康熙后期至乾隆七年间供奉内廷，并受到西洋绘画的一定影响。即“木犀”，木樨科，秋季开花，黄色或黄白色，极芳香，常见的有金桂、银桂、四季桂等，为珍贵的观赏芳香植物。“桂”按谐音为“贵”，带富贵之意，故常用“折桂”一词表示科举及第。'}
    mysql = Mysql('localhost', 'root', 'mysql', 'gugong')
    mysql.saveToDB(init_data)
