#K
#
# o
# h
# l
# c

class K():
    def __init__(self, data):
        self.Set(data)

    def Set(self, data):
        self.t = data[0];
        self.o = data[1];
        self.h = data[2];
        self.l = data[3];
        self.c = data[4];
        self.increase = (self.c - self.o) / self.o;
        self.amplitude = (self.h - self.l) / self.l;

    def __str__(self):
        return 't = {0}, o = {1}, h = {2}, l = {3}, c = {4}, increase = {5}, amplitude = {6}'.format(self.t, self.o, self.h, self.l, self.c, self.increase, self.amplitude);