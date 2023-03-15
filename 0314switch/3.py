# 总照片数
a = input()
# 允许重复次数
b = int(input())
list = []
for i in range(int(a)):
    c = int(input())
    if list.count(c) < b:
        list.append(c)

for i in list:
    print(i)
