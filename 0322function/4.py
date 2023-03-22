def add(a, b):
    # 将两个数字用0补齐，使得它们的长度相等
    n = max(len(a), len(b))
    a = a.zfill(n)
    b = b.zfill(n)
    # 从低位到高位依次计算每一位的和
    carry = 0  # 进位
    res = ''
    for i in range(n - 1, -1, -1):
        digit_sum = int(a[i]) + int(b[i]) + carry
        carry = digit_sum // 10
        res = str(digit_sum % 10) + res
    # 如果最高位有进位，则在结果前加上1
    if carry > 0:
        res = '1' + res
    return res


def multiply(a, b):
    # 将两个数字转换为整数
    a = int(a)
    b = int(b)
    # 计算乘积
    prod = a * b
    res = str(prod)
    return res if res else '0'


# 读入输入文件
with open('plus.in', 'r') as f:
    a = f.readline().strip()  # 第一行是超长正整数A
    op = f.readline().strip()  # 第二行只有一个字符"+"或"*"，分别代表加、乘运算
    b = f.readline().strip()  # 第三行是超长正整数B

# 进行运算
if op == '+':
    ans = add(a, b)
else:
    ans = multiply(a, b)

# 写入输出文件
with open('plus.out', 'w') as f:
    f.write(ans + '\n')
