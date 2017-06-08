#K
#
# o
# h
# l
# c
# vol
# increase
# amplitude

class DATA():
    def __init__(self)
        self.t =0;
        self.o = 0;
        self.h = 0;
        self.l = 0;
        self.c = 0;
        self.vol = 0;
        self.increase = 0;
        self.amplitude = 0;

    def Set(self, data):
        self.t = data[0];
        self.o = data[1];
        self.h = data[2];
        self.l = data[3];
        self.c = data[4];
        self.vol = data[5];
        self.increase = (self.c - self.o) / self.o;
        self.amplitude = (self.h - self.l) / self.l;
    
    def __str__(self):
        return 't = {0}, o = {1}, h = {2}, l = {3}, c = {4}, vol = {5}, increase = {6}, amplitude = {7}'.format(self.t, self.o, self.h, self.l, self.c, self.vol, self.increase, self.amplitude);

class K():
    def __init__(self, data):
        self.data = [];

    def Add(self, data);
        self.data.extend(data);

    def Input(self, data):
        for k, d in enumerate(data):
            dt = DATA()
            dt.Set(d);
            self.data.append(dt)
            
    def __str__(self):
        str = '';
        for k, v in enumerate(self.data):
            str = str + v.__str__() + '\n';
        return str;