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
    def __init__(self, type, idx):
        self.type = type;
        self.idx = idx;
    def __str__(self):
        return 'type:%s,idx:%d' % (self.type, self.idx);

class Wave():
    def __init__(self, point1, point2):
        self.point1 = point1;
        self.point2 = point2;

    def cal(self, ks):
        idx1 = self.point1.idx;
        idx2 = self.point2.idx;
        self.type   = self.point2.type; #'{0}{1}'.format(self.point1.type, self.point2.type);
        self.wmax   = MAX(ks.prices, idx1, idx2);
        self.wmin   = MIN(ks.prices, idx1, idx2);
        self.wvolume    = SUM(ks.volumes, idx1, idx2);
        self.wrmbvolume = SUM(ks.rmbvolumes, idx1, idx2);
        self.winterval  = idx2 - idx1;
        self.cvolume    = ks.volumes[idx2];
        self.crmbvolume = ks.rmbvolumes[idx2];
        self.cprice = ks.prices[idx2];
        self.ck     = ks[idx2];

        # self.height = (self.wmax - self.wmin) * self.winterval;
        self.volheight = self.wrmbvolume / self.winterval;
        self.height = (self.wmax - self.wmin)/self.winterval;
        if self.height == 0:
            self.height = self.winterval;
        if self.volheight == 0:
            self.volheight = self.winterval;

    def __str__(self):
        return 'type={0},idx1={1},idx2={2},height={3},min={4},max={5}'.format(self.type, self.point1.idx, self.point2.idx, self.height, self.wmin, self.wmax);

class MutliMovingAverage():
    def __init__(self, N1=5, N2=10, N3=21, N4=42):
        self.KLines = KLine();
        # price
        self.MA1 = [];
        self.MA2 = [];
        self.MA3 = [];
        self.MA4 = [];
        self.N1 = N1;
        self.N2 = N2;
        self.N3 = N3;
        self.N4 = N4;
        self.status = None;
        # volume
        self.VMA1 = [];
        self.VMA2 = [];
        self.rmbvolumeN3 = 0;
        # points
        self.points = [[], [], []];
        # wave
        self.waves = [[], [], []];
        # kdj
        self.KDJ = KDJ();
        # ma3 price wave point;
        # self.ma3rate = [];
        # self.wavepointm3 = WavePoint();
        #self.wavewavepointm3 = WavePoint();

    def Run(self, d, period=None, servertimestamp=None):
        if period and servertimestamp:
            data = d[-1];
            x = servertimestamp - data[0];
            if x < period:
                data[5] /= x; # virtual volume
        # k
        self.KLines.Input(d);
        # kdj
        self.KDJ.Input(self.KLines);
        # price
        MA(self.KLines.prices, self.MA1, self.N1);
        MA(self.KLines.prices, self.MA2, self.N2);
        MA(self.KLines.prices, self.MA3, self.N3);
        MA(self.KLines.prices, self.MA4, self.N4);
        # volume
        MA(self.KLines.volumes, self.VMA1, self.N1);
        MA(self.KLines.volumes, self.VMA2, self.N2);
        

        
        # ma3 rate and wavepoint;
        # RATE(self.MA3, self.ma3rate, self.N3);
        # self.wavepointm3.InputTrend(self.ma3rate);
        # self.wavewavepointm3.InputTrend(self.wavepointm3.points);


    def Export(self, path):
        if len(self.MA1) < 1:
            return ;
        f = open(path, 'wb');
        w = csv.writer(f);
        w.writerow(['index', 'MA1', 'MA2', 'MA3', 'MA4']);
        for k in range(0, len(self.MA1)):
            w.writerow([k, self.MA1[k], self.MA2[k], self.MA3[k], self.MA4[k]]);
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

    def Do(self):
        ret = {};
        k   = self.KLines.Get(-1);
        type=None;
        pwidx = 0;

        bc43 = CROSS(self.MA4, self.MA3);
        if bc43:
            self.status = 'sell';
            type = 'sell';
        sc34 = CROSS(self.MA3, self.MA4);
        if sc34:
            self.status = 'buy'
            type = 'buy';

        if self.status == 'buy' and type == None and True:
            type = self.KDJ.Do();
            if type:
                pwidx = 2;
                print "kdj:{0} time:{1}, c:{2}, k idx:{3}".format(type, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(k.t)), k.c, k.idx)

        if self.status == 'buy' and type == None and False:
            bc  = CROSS(self.MA2, self.MA1);
            if bc:
                print "mashort sell time:{0}, c:{1}, k idx:{2}".format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(k.t)), k.c, k.idx)
                type = 'sell';
                pwidx = 1;
            sc = CROSS(self.MA1, self.MA2);
            if sc:
                print "mashort buy time:{0}, c:{1}, k idx:{2}".format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(k.t)), k.c, k.idx)
                type = 'buy';
                pwidx = 1;

        if type != None:
            # frist update
            points = self.points[pwidx];
            waves = self.waves[pwidx];

            lenwaves    = len(waves);
            lenpoints   = len(points);
            pwave = None;
            cwave = None;
            cfwave = None;
            sort = 1000;
            p1 = None;
            p2 = None;
            
            if lenpoints > 0:
                p2 = points[-1];
                if p2.idx != k.idx:
                    np2 = Point(type, k.idx);
                    if p2.type == type:
                        points[-1] = np2;
                    else:
                        points.append(np2);
                    p2 = np2;
            else:
                p2 = Point(type, k.idx);
                points.append(p2);

            lenpoints = len(points)
            if lenpoints < 2:
                p1 = Point('buy', 0);
                if type == 'buy':
                    p1.type = 'sell';
            else:
                p1 = points[-2];

            if lenwaves > 0:
                cwave = waves[-1];
                if cwave.point2.idx == k.idx:
                    cwave.cal(self.KLines);
                if cwave.type == type:
                    cwave.point2 = p2;
                    cwave.cal(self.KLines);
                else:
                    ncwave = Wave(p1, p2);
                    ncwave.cal(self.KLines);
                    waves.append(ncwave);
                    cwave = ncwave;
            else:
                cwave = Wave(p1, p2);
                cwave.cal(self.KLines);
                waves.append(cwave);
            if lenwaves > 1:
                cfwave = waves[-2];
            if lenwaves > 2:
                pwave = waves[-3];
                if cwave and pwave and cfwave:
                    cpheight = cwave.height/pwave.height;
                    cpvolheight = cwave.volheight/pwave.volheight;
                    cfvolheight = 0
                    #cfvolheight = cwave.volheight/cfwave.volheight;
                    if pwidx == 0:
                        cpheight = pwave.height/cwave.height;
                        cpvolheight = pwave.volheight/cwave.volheight;
                        cfvolheight = 0;#cfwave.volheight/cwave.volheight;
                    sort = cpheight + cpvolheight + cfvolheight;
                    if pwidx == 1:
                        if type == 'buy':
                            if cwave.wmin < pwave.wmin and cwave.wmax < pwave.wmax:
                                type = None;
                                if cpheight < 1 and cpvolheight < 1 and cfvolheight < 1:
                                    type = 'buy'
                                else:
                                    print ' !!! wave buy cpheight:{0}, cpvolheight:{1}, cfvolheight:{2}, time:{3}'.format(cpheight, cpvolheight, cfvolheight, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(k.t)));
                        if type == 'sell':
                            type = None;
                            if cwave.wmax > pwave.wmax and cwave.wmin > pwave.wmin:
                                if cpheight < 1 and cpvolheight < 1 and cfvolheight < 1:
                                    type = 'sell';
                                else:
                                    print ' !!! wave sell cpheight:{0}, cpvolheight:{1}, cfvolheight:{2}, time:{3}'.format(cpheight, cpvolheight, cfvolheight, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(k.t)));    
                            else:
                                print ' !!! wave sell cpheight:{0}, cpvolheight:{1}, cfvolheight:{2}, time:{3}'.format(cpheight, cpvolheight, cfvolheight, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(k.t)));
            if pwidx != 0 and type == 'buy':
                p = self.points[0][-1];
                # sort = self.MA4[p.idx] / self.MA4[-1];
                if self.MA4[-1] - self.MA4[p.idx] < 0:
                    sort = -sort;
                #else:
                #    sort = 1/(self.MA4[-1] - self.MA4[p.idx]);

            ret['type']     = type;
            ret['cwave']    = cwave;
            ret['pwave']    = pwave;
            ret['cfwave']   = cfwave;
            ret['sort']     = sort;

        return ret;



