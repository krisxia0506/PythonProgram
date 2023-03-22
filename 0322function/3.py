def escape(s, t):
    """
    将字符串t拷贝到字符串s中,并在拷贝过程中将诸如换行符与制表符转换成诸如\n\t等换码序列.
    """
    t = t.replace('\n', '\\n')  # 将换行符转换为\n
    t = t.replace('\t', '\\t')  # 将制表符转换为\t
    s += t
    return s


t = ''  # 初始化字符串t为空字符串
for i in range(3):  # 循环3次
    line = input()  # 获取一行输入
    t += line + '\n'  # 将输入的行添加到t中，并加上换行符

s = ''  # 初始化字符串s为空字符串
s = escape(s, t)  # 将t拷贝到s中，并进行换码序列转换
print(s)  # 输出转换后的字符串s