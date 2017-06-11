# wave from point
# we can found a set of point
from formula.K import K;

class Direction():
    UP = 1;
    Down = 3;
'''
self.t = data[0];
self.o = data[1];
self.h = data[2];
self.l = data[3];
self.c = data[4];
self.vol = data[5];
'''
class Segment():
    def __init__(high, hightIndex, low, lowIndex):
        self.hk = K();
        self.hkidx = -1;
        self.lk = K();
        self.lkidx = -1;
        self.dir = Direction.UP;
    def InputOneK(idx, k):
        if self.hkidx == -1:
            self.hk = k;
            self.hkidx = idx;
            self.low = k;
            self.lkidx = idx;
            self.current = k;
        else:
            # k contain
            isContain = self.current.Contain(k);
            if isContain:
                if self.dir == Direction.UP:
                    self.current = K([0, 0, self.current.h, k.l, 0, 0]);
                else:
                    self.current = K([0, 0, k.h, self.current.l, 0, 0]);
            else:
                if self.current.h < k.h :
                    self.current = K([0, 0, k.h, max(k.l, self.current.l), 0, 0]);
                    self.hkidx = idx;
                else:
                    self.current = K([0, 0, min(k.h, self.current.h), k.l, 0, 0]);
                    self.lowIndex = idx;
                

class Wave():
    def __init__():
        self.data = [];
        self.segs = [];

    def Input(klines):
        lk = len(klines);
        ps = 0;
        if len(self.segs) > 0 :
            ps.
