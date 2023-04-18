# 数列翻转
numbers = list(map(eval, input().split()))
numbers = numbers[1:]
numbers.reverse()
for i in numbers:
    print(i, end=" ")

