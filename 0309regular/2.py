from re import findall


def func(text):
    a = findall(r'(\w)(?!.*\1)', text[::-1])
    return ''.join(a)[::-1]  # 随机字符串


print(func(input()))
