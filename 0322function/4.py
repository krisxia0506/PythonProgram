def add(a, b):
    carry = 0
    res = []
    i = len(a) - 1
    j = len(b) - 1
    while i >= 0 or j >= 0 or carry > 0:
        num1 = int(a[i]) if i >= 0 else 0
        num2 = int(b[j]) if j >= 0 else 0
        s = num1 + num2 + carry
        res.append(str(s % 10))
        carry = s // 10
        i -= 1
        j -= 1
    return ''.join(res[::-1])


def multiply(a, b):
    m = len(a)
    n = len(b)
    res = [0] * (m + n)
    for i in range(m - 1, -1, -1):
        carry = 0
        for j in range(n - 1, -1, -1):
            s = int(a[i]) * int(b[j]) + carry + res[i + j + 1]
            res[i + j + 1] = s % 10
            carry = s // 10
        res[i] += carry
    res = ''.join(map(str, res)).lstrip('0')
    return res if res else '0'


# 读入输入文件
with open('plus.in', 'r') as f:
    a = f.readline().strip()
    op = f.readline().strip()
    b = f.readline().strip()

# 进行运算
if op == '+':
    ans = add(a, b)
else:
    ans = multiply(a, b)

# 写入输出文件
with open('plus.out', 'w') as f:
    f.write(ans + '\n')
