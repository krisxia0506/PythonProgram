def insert(a, b):
    count = a + b
    lst = list(count)
    lst.sort()
    for items in lst:
        print(items, end="")


string = input()
c = input()
insert(string, c)
