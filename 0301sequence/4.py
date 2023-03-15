# 数字出现次数排序
from collections import Counter

input()
a = sorted(list(map(int, input().split())))
count = dict(Counter(a))
count = sorted(count.items(), key=lambda x: x[1], reverse=True)
for key, value in count:
    print(str(key) + " " + str(value))

