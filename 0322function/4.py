# 在 Python 中，整数类型是有限制的，其范围取决于所占用的内存大小。
# 在本题中，输入的数字最长可达 50 位，这已经远远超过了 Python 整数类型的表示范围，
# 因此不能直接使用 Python 提供的整数类型进行加法运算。
# 为了处理超长正整数的加法，需要将输入的字符串形式的数字逐位相加，并注意处理进位。
# 因此，我们需要将字符串转换成数字，然后逐位相加，最后再将结果转换回字符串形式输出。
# 另外，两个输入数字的位数可能不同，需要先对齐位数，即在短的数字前面补0，使得两个数字位数相同。
def add(a, b):
    # 将两个数字用0补齐，使得它们的长度相等
    n = max(len(a), len(b))
    a = a.zfill(n)
    b = b.zfill(n)
    # 从低位到高位依次计算每一位的和
    carry = 0  # 进位
    res = ''  # 结果
    for i in range(n - 1, -1, -1):
        digit_sum = int(a[i]) + int(b[i]) + carry
        # 13//10=1, 13%10=3
        carry = digit_sum // 10  # 计算进位
        # res = 余数 + 之前的结果
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
