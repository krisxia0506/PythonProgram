def gen():
    for x in range(10):
        yield x


def xx(iter):
    for x in iter:
        if x == 3:
            break
    for x in iter:
        yield x


def print_iter(iter):
    for x in iter:
        print(x)


def skip_count(count: int, iter):
    for _ in range(count):
        next(iter)
    return iter


def dropwhile(predict, iter):
    for x in iter:
        if not predict(x):
            yield x
            break
    for x in iter:
        yield x


# from itertools import dropwhile

print_iter(skip_count(1, dropwhile(lambda x: x != 3, gen())))
