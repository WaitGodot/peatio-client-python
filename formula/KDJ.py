'''
RSV:=(CLOSE-LLV(LOW,N))/(HHV(HIGH,N)-LLV(LOW,N))*100;
K:SMA(RSV,M1,1);
D:SMA(K,M2,1);
J:3*K-2*D;
'''
from formula.Formula import HIGH
from formula.Formula import LOW
from formula.Formula import SMA
import csv

class DATA():
    def __init__(self, k, d, j):
        self.k = k;
        self.d = d;
        self.j = j;
    def __str__(self):
        return 'k={0},d={1},j={2}'.format(self.k, self.d, self.j);

class KDJ():
    def __init__(self, N1=9, N2=3, N3=3):
        self.N1 = N1;
        self.N2 = N2;
        self.N3 = N3;
        self.hightArr = [];
        self.lowArr = [];
        self.RSV = [];
        self.K = [];
        self.D = [];
        self.J = [];

    def Input(self, klines):
        l = len(self.hightArr);
        prices = klines.prices;
        count = len(prices) - l;

        HIGH(klines.ToList('h'), self.hightArr, self.N1);
        LOW(klines.ToList('l'), self.lowArr, self.N1);
        
        for idx in range(l, count):
            rsv = (prices[idx] - self.lowArr[idx]) / (self.hightArr[idx] - self.lowArr[idx]) * 100;
            self.RSV.append(rsv);
       
        l = len(self.K);
        count = len(self.RSV) - l;
        for idx in range(l, count):
            SMA(self.RSV, self.K, self.N2, 1);

        l = len(self.D);
        count = len(self.K) - l;
        for idx in range(l, count):
            SMA(self.K, self.D, self.N3, 1)
       
        l = len(self.J);
        count = len(self.K) - l;
        for idx in range(l, count):
            self.J.append(self.K[idx] * 3 - self.D[idx] * 2);

    def Get(self, idx):
        return DATA(self.K[idx], self.D[idx], self.J[idx]);

    def Export(self, path):
        f = open(path, 'wb');
        w = csv.writer(f);
        for k, v in enumerate(self.K):
            w.writerow([k,v]);

        f.close();

    def __str__(self):
        str = '';
        l = len(self.K);
        for k in range(0, l):
            str = str + self.Get(indx).__str__() + '\n';
        return str;
    def __len__(self):
        return len(self.K);
