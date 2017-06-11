#K
#
# o
# h
# l
# c
# vol
# increase
# amplitude
from formula.Formula import High;
from formula.Formula import Low;

class K():
    def __init__(self, data=None):
        if data:
            self.Set(data);
        else:
            self.Set([0,0,0,0,0,0]);

    def Set(self, data):
        self.t = data[0];
        self.o = data[1];
        self.h = data[2];
        self.l = data[3];
        self.c = data[4];
        self.vol = data[5];
        self.increase = (self.c - self.o) / self.o;
        self.amplitude = (self.h - self.l) / self.l;
    def Contain(self, ohterk):
        if self.h >= ohterk.h & self.l < self.l :
            return True;
        return False;

    def __getitem__(self, k):
        if k == 't':
            return self.t;
        if k == 'o':
            return self.o;
        if k == 'h':
            return self.h;
        if k == 'l':
            return self.l;
        if k == 'c':
            return self.c
        if k == 'vol':
            return self.vol;
        if k == 'increase':
            return self.increase;
        if k == 'amplitude':
            return self.amplitude;

    def __str__(self):
        return 't = {0}, o = {1}, h = {2}, l = {3}, c = {4}, vol = {5}, increase = {6}, amplitude = {7}'.format(self.t, self.o, self.h, self.l, self.c, self.vol, self.increase, self.amplitude);

class KLine():
    def __init__(self):
        self.data = [];
        self.prices = []; # use close price

    def Input(self, data):
        last = None;
        if len(self.data) > 0:
            last = self.data[-1];
        for k, d in enumerate(data):
            if last:
                if d[0] <= last.t:
                    continue;
            self.data.append(K(d))
            
    def ToList(self, key, N=None):
        ret = [];
        if N == None:
            for k, d in enumerate(self.data):
                ret.append(d[k]);
        else:
            for idx in range(1, N):
                if len(self.data) >= idx:
                    ret.append(self.data[-idx][key]);

        return ret;
    
    def High(self, key, N):
        return High(self.ToList(key));

    def __str__(self):
        str = '';
        for k, v in enumerate(self.data):
            str = str + v.__str__() + '\n';
        return str;