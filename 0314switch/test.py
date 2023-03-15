# for i in "CHINA":
#     for k in range(2):
#         print(i, end="")
#         if i == 'N':
#             break

# for num in range(1,4):
#     sum *= num
# print(sum)
#
# for s in "HelloWorld":
#     if s=="W":
#         continue
#     print(s,end="")
#
# for i in "Python":
#     print(i,end=" ")
#
# a=3
# while a > 0:
#     a -= 1
#     print(a,end=" ")
#
# sum = 0
# for i in range(1,11):
#     sum += i
#     print(sum)
#
# age=23
# start=2
# if age%2!=0:
#     start=1
# for x in range(start,age+2,2):
#     print(x)
# k=10000
# while k>1:
#     print(k)
#     k=k/2
# for i in "Summer":
#     if i == "m":
#         break
#         print(i)

n=eval(input())
for i in range(1,n,2):
    print("*" * i)