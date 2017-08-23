# rule
# 
#
from formula.K import KLine
from formula.MACD import MACD
from formula.KDJ import KDJ
from RebotConfig import RebotConfig
from rule.WaveKline import WaveKline
from rule.WavePoint import WavePoint
from rule.WaveKline import Direction

from formula.Formula import *

import time
import math
import csv

class Point():
    def __init__(self, type, idx, angle):
        self.type = type,
        self.idx = idx;
        self.angle = angle;

class Wave():
    def __init__(self, point1, point2):
        self.point1 = point1;
        self.point2 = point2;

    def cal(self, ks):
        idx1 = self.point1.idx;
        idx2 = self.point2.idx;
        self.type   = '{0}{1}'.format(self.point1.type, self.point2.type);
        self.wmax   = MAX(ks.prices, idx1, idx2);
        self.wmin   = MIN(ks.prices, idx1, idx2);
        self.wvolume    = SUM(ks.volumes, idx1, idx2);
        self.winterval  = idx2 - idx1;
        self.cvolume    = ks.volumes[idx2];
        self.cprice = ks.prices[idx2];

        self.height = (self.wmax - self.wmin) * self.winterval;
    def __str__(self):
        print ''

class MutliMovingAverage():
    def __init__(self, N1=5, N2=10, N3=31):
        self.KLines = KLine();
        # price
        self.MA1 = [];
        self.MA2 = [];
        self.MA3 = [];
        self.N1 = N1;
        self.N2 = N2;
        self.N3 = N3;
        # volume
        self.VMA1 = [];
        self.VMA2 = [];
        # points
        self.points = [];
        # wave
        self.waves = [];
        # self.client = Client(access_key=RebotConfig.access_key, secret_key=RebotConfig.secret_key)

    def Run(self, d, period=None, servertimestamp=None):
        # d = self.client.get(get_api_path('k'), params={'market': '{0}cny'.format(self.market), 'limit':100,'period' : '{0}'.format(self.period)});
        # print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(d[0][0]));
        if period and servertimestamp:
            data = d[-1];
            x = servertimestamp - data[0];
            if x < period:
                data[5] /= x; # virtual volume
        self.KLines.Input(d);
        # price 
        MA(self.KLines.prices, self.MA1, self.N1);
        MA(self.KLines.prices, self.MA2, self.N2);
        MA(self.KLines.prices, self.MA3, self.N3);
        # volume
        MA(self.KLines.volumes, self.VMA1, self.N1);
        MA(self.KLines.volumes, self.VMA2, self.N2);


    def Export(self, path):
        if len(self.MA1) < 1:
            return ;
        f = open(path, 'wb');
        w = csv.writer(f);
        w.writerow(['index', 'MA1', 'MA2', 'MA3']);
        for k in range(0, len(self.MA1)):
            w.writerow([k, self.MA1[k], self.MA2[k], self.MA3[k]]);
        f.close();

    def ExportWave(self, path):
        if len(self.waves) < 0:
           return;
        f = open(path, 'wb');
        wcsv = csv.writer(f);
        wcsv.writerow(['index', 'type', 'point1.idx', 'point2.idx', 'wmax', 'wmin', 'wvolume', 'winterval', 'cvolume', 'cprice']);
        for k in range(0, len(self.waves)):
            w = self.waves[k];
            wcsv.writerow([k, w.type, w.point1.idx, w.point2.idx, w.wmax, w.wmin, w.wvolume, w.winterval, w.cvolume, w.cprice]);
        f.close();

    def Angle(self):
        lenma = len(self.MA3);
        if lenma < 2:
            return 0;
        dz = self.MA3[-1] - self.MA3[-2];
        l = math.sqrt(1 + dz * dz);
        return math.asin(dz/l);

    def Do(self):
        k = self.KLines.Get(-1);
        bc = CROSS(self.MA2, self.MA1);
        a = self.Angle();
        type=None;
        if bc:
            print "sell time:{0}, ma3 angle:{1}, ma3:{2}, c:{3}".format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(k.t)), a, self.MA3[-1], k.c)
            if a > 0 and self.MA3[-1] < k.c:
                print "sell fail"
            else:
                type='sell';
            type='sell';
        sc = CROSS(self.MA1, self.MA2);
        if sc:
            print "buy time:{0}, ma3 angle:{1}, ma3:{2}, c:{3}".format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(k.t)), a, self.MA3[-1], k.c)
            # if a <= 0 and self.MA3[-1] > k.c:
            if a < 0:
                print "buy fail"
            else:
                type='buy';
            type='buy';
        if type!=None:
            p1 = None;
            p2 = Point(type, k.idx, a);
            self.points.append(p2);
            if len(self.points) <= 1:
                p1 = Point('buy', 0, 0);
                if type == 'buy':
                    p1.type = 'sell';
            else:
                p1 = self.points[-2];
            w = Wave(p1, p2);
            w.cal(self.KLines);
            self.waves.append(w);

            lenwaves = len(self.waves);
            if lenwaves > 2:
                for idx in range(0, lenwaves-1):
                    nw = self.waves[lenwaves-idx-1-1];
                    if nw.type == w.type:
                        if nw.height != 0 and w.height / nw.height > 1.2:
                            print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!! w height:{0}, nw height:{1}, time:{2}'.format(w.height, nw.height, k.t);
                            type = None;
                            break;




        #bc = CROSS(self.MA3, self.MA1);
        #if bc:
        #    print "sell m3 cross m1 0 time:{0}, ma3 angle:{1}, ma3:{2}, c:{3}".format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(k.t)), a, self.MA3[-1], k.c)
        #    return 'sell';
        return type;


        
