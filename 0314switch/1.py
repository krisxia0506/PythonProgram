a = input()
output = ""
for i in a:
    # 判断是否为大写字母
    if output == "":
        output += i.lower()
    elif i.isupper():
        output += "_"
        # 转换为小写字母
        output += i.lower()
    else:
        output+=i
print(output)

