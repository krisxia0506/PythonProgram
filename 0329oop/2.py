import math


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def dist_from(self, p2):
        return ((self.x - p2.x) ** 2 + (self.y - p2.y) ** 2 + (self.z - p2.z) ** 2) ** 0.5


x1, y1, z1 = input().split()
x1 = float(x1)
y1 = float(y1)
z1 = float(z1)
p1 = Point(x1, y1, z1)
x2, y2, z2 = input().split()
x2 = float(x2)
y2 = float(y2)
z2 = float(z2)
p2 = Point(x2, y2, z2)
print("%.2f" % p1.dist_from(p2))
