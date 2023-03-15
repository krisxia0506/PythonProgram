a = input()
alist = a.split()
alist = [x.capitalize() for x in alist]
c = len(alist)
if c == 1:
    print(a.capitalize())
elif c == 2:
    print(alist[0], alist[1])
else:
    m = alist[0]
    n = alist[-1]
    alist.remove(alist[0])
    alist.remove(alist[-1])
    alist = [j[0] for j in alist]
    y = ". ".join(alist)
    print(m, y + ".", n)
