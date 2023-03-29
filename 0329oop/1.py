class Rect():
    def __init__(self, len, wid):
        self.len = len
        self.wid = wid

    def area(self):
        area = self.len * self.wid
        return area


x = float(input())
y = float(input())
r1 = Rect(x, y)
print(r1.area())
