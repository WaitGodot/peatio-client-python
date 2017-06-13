# wave from point
# we can found a set of point
from formula.K import K;

SegmentMinCount = 3;

class Direction():
    UP = 1;
    FLAT = 2;
    DOWN = 3;
'''
self.t = data[0];
self.o = data[1];
self.h = data[2];
self.l = data[3];
self.c = data[4];
self.vol = data[5];
'''

def ToStringDir(dir):
    if dir == Direction.UP:
        return 'UP';
    if dir == Direction.FLAT:
        return 'FLAT';
    if dir == Direction.DOWN:
        return 'DOWN';

def CalDir(k0, k1, k2):
    if k0 == None or k1 == None or k2 == None:
        return Direction.FLAT;
    if k0.h < k1.h and k1.h < k2.h:
        return Direction.UP;
    if k0.l > k1.l and k1.l > k2.l:
        return Direction.DOWN;
    return Direction.FLAT;

class Segment():
    def __init__(self):
        self.hkidx = -1;
        self.lkidx = -1;
        self.dir = Direction.FLAT;
        self.ks = [];
    def InputOneK(self, idx, k):
        if self.hkidx == -1:
            self.hk = k;
            self.hkidx = idx;
            self.lk = k;
            self.lkidx = idx;
            self.k0 = k;
            self.k1 = k;
            self.k2 = k;
        else:
            # k contain
            isContain = self.k2.Contain(k) or k.Contain(self.k2);
            if isContain:
                if self.dir == Direction.UP:
                    self.k2 = K([k.t, 0, self.k2.h, k.l, 0, self.k2.vol + k.vol]);
                if self.dir == Direction.DOWN:
                    self.k2 = K([k.t, 0, k.h, self.k2.l, 0, 0]);
            else:
                if self.k2.h <= k.h :
                    nk = K([k.t, 0, k.h, max(k.l, self.k2.l), 0, 0]);
                if self.k2.l >= k.l :
                    nk = K([k.t, 0, min(k.h, self.k2.h), k.l, 0, 0]);
                self.k0 = self.k1; 
                self.k1 = self.k2;
                self.k2 = nk;
                self.ks.append(nk);
        if self.lk.l > k.l:
            self.lkidx = idx;
            self.lk = k;
        if self.hk.h < k.h:
            self.hkidx = idx;
            self.hk = k;

        ndir = CalDir(self.k0, self.k1, self.k2);
        if self.dir == ndir or ndir == Direction.FLAT or self.dir == Direction.FLAT:
            if ndir != Direction.FLAT and self.dir == Direction.FLAT:
                self.dir = ndir;
            return True;
        else:
            return False;

    def __str__(self):
        return 'dir:{0}, high:{1}, high idx:{2}, low:{3}, low idx:{4}'.format(ToStringDir(self.dir), self.hk.h, self.hkidx, self.lk.l, self.lkidx);
                

class WaveKline():
    def __init__(self):
        self.data = [];
        self.segs = [];
        self.segs.append(Segment());
        self.idx = 0;

    def Input(self, klines):
        lk = len(klines);
        ps = self.segs[-1];
        for idx in range(self.idx, lk):
            # print idx, klines[idx];
            rt = ps.InputOneK(idx, klines[idx])
            if rt == False :
                ps = Segment();
                ps.InputOneK(idx - 2, klines[idx - 2]);
                ps.InputOneK(idx - 1, klines[idx - 1]);
                ps.InputOneK(idx, klines[idx]);
                self.segs.append(ps);
        self.idx = lk;
    
    def Export(self, path):
        print '';

    def __str__(self):
        str = '';
        for k, seg in enumerate(self.segs):
           str = str + seg.__str__() + '\n';
        return str;
    


