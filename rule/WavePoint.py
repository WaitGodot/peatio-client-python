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
        else:
            self.fd0 = self.fd1;
            self.fd1 = self.fd2;
            self.fd2 = fd;
            
        if self.high < fd:
            self.high = fd;
            self.highidx = idx;
        if self.low > fd:
            self.low = fd;
            self.lowidx = idx;
        ndir = CalDir(self.fd0, self.fd1, self.fd2);
        print idx, fd, ndir, self.dir;
        if self.dir == ndir or ndir == Direction.FLAT or self.dir == Direction.FLAT:
            if ndir != Direction.FLAT and self.dir == Direction.FLAT:
                self.dir = ndir;
            return True;
        else:
            return False;
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
        for idx in range(self.idx, lk - 1):
            rt = ps.InputOneFloat(idx, fds[idx])
            if rt == False :
                ps = Segment();
                ps.InputOneFloat(idx - 2, fds[idx - 2]);
                ps.InputOneFloat(idx - 1, fds[idx - 1]);
                ps.InputOneFloat(idx, fds[idx]);
                self.segs.append(ps);
        self.idx = lk;
    
    def Export(self, path):
        print '';

    def __str__(self):
        str = '';
        for k, seg in enumerate(self.segs):
           str = str + seg.__str__() + '\n';
        return str;
    