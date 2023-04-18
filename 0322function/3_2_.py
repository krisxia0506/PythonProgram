import sys

a = sys.stdin.read()
b = a.replace("\n", "\\n")
c = b.replace("\t", "\\t")

print(c)

