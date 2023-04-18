# 方法判断是否为素数
def is_prime(n):
    if n == 1:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True


a = input()
if is_prime(int(a)) and is_prime(int(a[::-1])):
    print('yes')
else:
    print('no')
