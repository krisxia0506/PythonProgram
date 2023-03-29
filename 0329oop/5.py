class Time():
    def __init__(self):
        self.hour = 0;
        self.minute = 0;
        self.second = 0;

    def setTime(self, h, m, s):
        self.hour = h
        self.minute = m
        self.second = s

    def showTime(self):
        print(str(self.hour) + ':' + str(self.minute) + ':' + str(self.second))


    def nextHour(self):
        if self.hour == 23:
            self.hour = 0
        else:
            self.hour = self.hour + 1


t = Time()
t.showTime()

h, m, s = input().split()
h = int(h)
m = int(m)
s = int(s)

t.setTime(h, m, s)
t.showTime()
t.nextHour()
t.showTime()
