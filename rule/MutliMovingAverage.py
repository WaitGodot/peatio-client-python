# rule
# 
#
from formula.K import KLine
from formula.MACD import MACD
from formula.KDJ import KDJ
from formula.Formula import CROSS
from formula.Formula import MA
from RebotConfig import RebotConfig
from rule.WaveKline import WaveKline
from rule.WavePoint import WavePoint
from rule.WaveKline import Direction

import time
import math
import csv

class MutliMovingAverage():
    def __init__(self, N1=5, N2=10, N3=31):
        self.KLines = KLine();
        self.MA1 = [];
        self.MA2 = [];
        self.MA3 = [];
        self.N1 = N1;
        self.N2 = N2;
        self.N3 = N3;
        # self.client = Client(access_key=RebotConfig.access_key, secret_key=RebotConfig.secret_key)

    def Run(self, d):
        # d = self.client.get(get_api_path('k'), params={'market': '{0}cny'.format(self.market), 'limit':100,'period' : '{0}'.format(self.period)});
        # print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(d[0][0]));
        self.KLines.Input(d);
        MA(self.KLines.prices, self.MA1, self.N1);
        MA(self.KLines.prices, self.MA2, self.N2);
        MA(self.KLines.prices, self.MA3, self.N3);
        self.Export("C:\\Users\\randy\\k.csv");
    def Export(self, path):
        if len(self.MA1) < 1:
            return ;
        f = open(path, 'wb');
        w = csv.writer(f);
        for k in range(0, len(self.MA1)):
            w.writerow([k, self.MA1[k], self.MA2[k], self.MA3[k]]);
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
        if bc:
        #    print "sell time:{0}, ma3 angle:{1}, ma3:{2}, c:{3}".format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(k.t)), a, self.MA3[-1], k.c)
        #    if a > 0 and self.MA3[-1] < k.c:
        #        print "sell fail"
        #        return None;
            return 'sell';
        sc = CROSS(self.MA1, self.MA2);
        if sc:
            print "buy time:{0}, ma3 angle:{1}, ma3:{2}, c:{3}".format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(k.t)), a, self.MA3[-1], k.c)
        #    if a <= 0 and self.MA3[-1] > k.c:
        #        print "buy fail"
        #        return None;
            return 'buy';
        bc = CROSS(self.MA3, self.MA1);
        #if bc:
        #    print "sell m3 cross m1 0 time:{0}, ma3 angle:{1}, ma3:{2}, c:{3}".format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(k.t)), a, self.MA3[-1], k.c)
        #    return 'sell';
        return None


        
