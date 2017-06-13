# wave for float data

from rule.WaveKline import Direction
from rule.WaveKline import ToStringDir

def CalDir(fd0, fd1, fd2):
    if fd0 < fd1 and fd1 < fd2:
    	return Direction.UP;
    if fd0 > fd1 and fd1 > fd2:
        return Direction.DOWN;
    return Direction.FLAT;

class Segment():
    def __init__(self):
        self.highidx = -1;
        self.lowidx = -1;
        self.high = 0;
        self.low = 0;
        self.dir = Direction.FLAT;

    def InputOneFloat(self, idx, fd):
        if self.highidx == -1:
            self.high = fd;
            self.highidx = idx;
            self.low = fd;
            self.lowidx = idx;
            self.fd0 = fd;
            self.fd1 = fd;
            self.fd2 = fd;
            
        ndir = CalDir(self.fd1, self.fd2, fd);
        isContain = False;
        # point contain
        if self.dir == Direction.UP:
            if fd < self.fd2 and fd > self.fd1:
                self.fd1 = fd; isContain = True;
            elif fd > self.fd2 and fd < self.fd1:
                self.fd2 = fd; isContain = True;
            else:
                self.fd0 = self.fd1; self.fd1 = self.fd2; self.fd2 = fd;
        elif self.dir == Direction.DOWN:
            if fd > self.fd2 and fd < self.fd1:
                self.fd1 = fd; isContain = True;
            elif fd < self.fd1 and fd > self.fd1:
                self.fd2 = fd; isContain = True;
            else:
                self.fd0 = self.fd1; self.fd1 = self.fd2; self.fd2 = fd;
        else:
            self.fd0 = self.fd1; self.fd1 = self.fd2; self.fd2 = fd;
        
        if isContain:
            return True, -1;
        if self.dir != ndir and ndir != Direction.FLAT: # break
            if self.dir == Direction.UP:
                return False, self.highidx;
            if self.dir == Direction.DOWN:
                return False, self.lowidx;
        return True, -1;

    def __str__(self):
        return 'dir:{0}, high:{1}, high idx:{2}, low:{3}, low idx:{4}'.format(ToStringDir(self.dir), self.high, self.highidx, self.low, self.lowidx);

class WavePoint():
    def __init__(self):
        self.segs = [];
        self.segs.append(Segment());
        self.idx = 0;

    def Input(self, fds):
        lk = len(fds);
        ps = self.segs[-1];
        print fds;
        for idx in range(self.idx, lk):
            rt, index = ps.InputOneFloat(idx, fds[idx])
            if rt == False :
                ps = Segment();
                for k in range(index, idx - index):
                    ps.InputOneFloat(k, fds[k]);
                self.segs.append(ps);
        self.idx = lk;
    
    def Export(self, path):
        print '';

    def __str__(self):
        str = '';
        for k, seg in enumerate(self.segs):
           str = str + seg.__str__() + '\n';
        return str;
    