# 判断两个数据集是否相同
from collections import Counter

input()
a = sorted(list(map(int, input().split())))
input()
b = sorted(list(map(int, input().split())))
if Counter(a) == Counter(b):
    print("1")
else:
    print("0")
count = dict(Counter(a))
for key, values in count.items():
    print(str(key) + " " + str(values))
