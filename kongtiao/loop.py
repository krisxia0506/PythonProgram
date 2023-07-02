start = 1
end = 20
for i in range(1, 5):  # ABCD区
    i = i * 1000
    for j in range(1, 7):  # 1-6楼
        j = j * 100
        a = i + j + start  # 1101
        b = i + j + end  # 1120
        for room in range(a, b + 1):
            print(room)