n = int(input())
dic = {}
# 马
for i in range(n):
    name, num = input().split(" ")
    dic[name] = int(num)
# 刘
m = int(input())
for j in range(m):
    name, num = input().split(" ")
    if name in dic.keys():
        dic[name] += int(num)
    else:
        dic[name] = int(num)
select_goods = input()
print(dic[select_goods])
