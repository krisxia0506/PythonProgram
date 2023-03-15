import re

a = input()


def fun(s: str):
    return (re.sub(r"([ ,.])i([ ,.])", "\g<1>I\g<2>", s.strip().capitalize()) + '.') if s else " "


print((" ".join((fun(s) for s in a.split("."))).strip()))
