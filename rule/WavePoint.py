# wave for float data

from rule.WaveKline import Direction
from rule.WaveKline import ToStringDir
import csv

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
        
        # print idx, ndir, self.dir, isContain, fd;
        if self.dir == Direction.FLAT:
            self.dir = ndir;
        if isContain:
            return True, -1;
        if self.dir != ndir and ndir != Direction.FLAT: # break
            if self.dir == Direction.UP:
                return False, self.highidx;
            if self.dir == Direction.DOWN:
                return False, self.lowidx;
        if ndir != Direction.FLAT or self.dir == Direction.FLAT:
            if self.high < fd:
                self.high = fd; self.highidx = idx;
            if self.low > fd:
                self.low = fd; self.lowidx = idx; 
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
        for idx in range(self.idx, lk):
            rt, index = ps.InputOneFloat(idx, fds[idx])
            if rt == False :
                # print 'insert new segment'
                ps = Segment();
                for k in range(index, idx+1):
                    ps.InputOneFloat(k, fds[k]);
                self.segs.append(ps);
        self.idx = lk;
    
    def Export(self, path):
        f = open(path, 'wb');
        w = csv.writer(f);
        l = len(self.segs);
        for k, v in enumerate(self.segs):
            if v.dir == Direction.UP:
                w.writerow([k, v.low]);
            else:
                w.writerow([k, v.high]);
            if k == l - 1:
                if v.dir == Direction.UP:
                    w.writerow([k, v.high]);
                else:
                    w.writerow([k, v.low]);

        f.close();
    def ToPoints(self):
        l = len(self.segs);
        rt = []
        for k, v in enumerate(self.segs):
            if v.dir == Direction.UP:
                rt.append(v.low);
            else:
                rt.append(v.high);
            if k == l - 1:
                if v.dir == Direction.UP:
                    rt.append(v.high);
                else:
                    rt.append(v.low);

    def __str__(self):
        str = '';
        for k, seg in enumerate(self.segs):
           str = str + seg.__str__() + '\n';
        return str;
    