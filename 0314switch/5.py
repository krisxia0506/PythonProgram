n = input()
dict= {}
for i in range(int(n)):
    a = input()
    if a == "Q":
        b = input()
        if b not in dict.keys():
            print("NONE")
        else:
            print(dict[b])
    elif a == "A":
        name,num = input().split()
        if name not in dict.keys():
            dict[name] = int(num)



