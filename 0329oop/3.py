class Student():
    def __init__(self, math, eng, pro):
        self.sno = 0
        self.name = ""
        self.mathScore = math
        self.engScore = eng
        self.proScore = pro

    def average(self):
        return (self.mathScore + self.engScore + self.proScore) / 3


m, e, p = input().split()
m = float(m)
e = float(e)
p = float(p)
s = Student(m, e, p)
print(s.average())