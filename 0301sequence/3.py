# 歌德巴赫猜想
a = int(input())


# 是否是素数
def is_prime(num):
    if num > 1:
        for i in range(2, num):
            if (num % i) == 0:
                break
        else:
            return 1


def is_pr(n):
    for i in range(2, n):
        for j in range(2, n):
            if is_prime(i) == 1 and is_prime(j) == 1 and i <= j:
                if i + j == n:
                    print(str(n) + "=" + str(i) + "+" + str(j))
                    # 这里return是为了防止重复输出
                    return
                else:
                    continue


for i in range(2, a + 1, 2):
    is_pr(i)
