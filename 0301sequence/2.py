# 找对称数

number = input().split(" ")
result = []


def check_if(number):
    if number[0] == number[3] and number[1] == number[2]:
        return 1
    else:
        return 0


for i in number:
    if check_if(i) == 1:
        result.append((i))
for k in result:
    print(k, end=" ")
print(len(result))
