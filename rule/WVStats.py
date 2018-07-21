
from formula.K import KLine
from formula.MACD import MACD
from formula.KDJ import KDJ
from RebotConfig import RebotConfig
from rule.WaveKline import WaveKline
from rule.WavePoint import WavePoint
from rule.WaveKline import Direction

from Log import Log
from formula.Formula import *

import time
import math
import csv

MAXKCOUNT = 10;
VOLTIMES = 2.2;
MAXBETA = 0.1;

class WVStats():
    def __init__(self, ValueN=10):
        self.KLines = KLine();
        self.Value = [];
        self.Volume = [];
        self.ValueN = ValueN;
        self.status = None;
        self.statuscost = 0;
        self.statusbuycurrent = 0;
        self.statusdelay = 0;
        self.stats = [];
        self.High = [];
        self.Low = [];
        self.lastidx = 0;
        self.lastbuyidx = 0;

    def Export(self, path):
        f = open(path, 'wb');
        w = csv.writer(f);
        w.writerow(['increase', 'amplitude', 'close', 'vol', 'value', 'volume', 'increase', 'amplitude', 'close', 'vol', 'value', 'volume', 'increase', 'amplitude', 'close', 'vol', 'value', 'volume', 'increase', 'amplitude', 'close', 'vol', 'value', 'volume', 'increase', 'amplitude', 'close', 'vol', 'value', 'volume']);
        for k, arr in enumerate(self.stats):
            d = [];
            for i in range(0,len(arr)):
                nd = arr[i];
                d.append(nd['k'].increase)
                d.append(nd['k'].amplitude)
                d.append(nd['k'].c)
                d.append(nd['k'].vol)
                d.append(nd['value'])
                d.append(nd['volume'])

            w.writerow(d);
        f.close();
        return;

    def Run(self, d, period=None, servertimestamp=None):
        if len(d) == 0:
            return ;
        self.lastidx = self.KLines.Input(d);

        MA(self.KLines.prices, self.Value, self.ValueN);
        MA(self.KLines.volumes, self.Volume, self.ValueN);
        HIGH(self.KLines.prices, self.High, self.ValueN*2);
        LOW(self.KLines.prices, self.Low, self.ValueN*2);
        if len(self.KLines) > self.ValueN + 1:
            return self.Do();
        return {'type':None};

    def Do(self, idx=-1, ignore=False):
        summ, ccount = self.KLines.Sum(12);
        summb = round(summ/5000000, 2);
        avgp = self.KLines.Ref(12, 'c', -2);
        prek = self.KLines.Get(idx - 1);
        prevolume = self.Volume[idx - 1];
        prevalue = self.Value[idx - 1];

        k = self.KLines.Get(idx);
        value = self.Value[idx];
        volume = self.Volume[idx];
        phigh = self.High[-2];
        plow = self.Low[-2];

        ret = {};
        ret['type'] = None;
        ret['k']    = k;
        ret['sort'] = 1;
        ret['angle'] = 10;
        ret['ext'] = {'summ' : summb}

        statslen = len(self.stats)
        for i in range(0, statslen):
            nk = statslen - i - 1;
            arr = self.stats[nk];
            if len(arr) < 5:
                arr.append({'k':k, 'value':value, 'volume':volume});

        self.stats.append([]);

        dv = 1;
        avgpp = 0;
        if avgp > 0:
            avgpp = round((k.c - avgp) / avgp *100, 2);
        else:
            print '\t\tavgp is eq 0', avgp;
        # print "xxxx", self.lastidx, self.statusbuycurrent, self.statusdelay, self.status;
        if self.status == 'buy':
            bk = self.KLines.Get(self.lastbuyidx);
            
            dv = (self.statuscost - self.statusbuycurrent)/self.statuscost * 2 + 1;
            dv = round(dv,2);
            scale = (self.statuscost - k.c)/self.statuscost > MAXBETA * dv;
            delay = (self.lastidx - self.statusdelay) > MAXKCOUNT * dv;
            # print (self.statuscost - k.c)/self.statuscost, MAXBETA * dv, dv, self.statusdelay, MAXKCOUNT * dv, prek.c > prevalue, prek.vol / (VOLTIMES * prevolume);
            avgscale = (k.c - self.statusbuycurrent)/self.statuscost*100;
            avgscale = round(avgscale,2);
            
            # delayw =  avgpp < 0 or avgpp > 5 * summ / 5000000;
            delayw =  False; #avgpp < 0 ;# or avgscale < 5*summ/5000000;
            if bk.increase * 100 > 15 * dv:
                delayw = True;
                print 'buy k increase'. bk.increase;
            if scale or delayw or delay or avgscale < -7:
                ret['type'] = 'sell';
                ret['ext']['dv'] = dv;
                ret['ext']['scale'] = scale;
                ret['ext']['avgscale'] = avgscale;
                ret['ext']['delay'] = delay;
                ret['ext']['avgpp'] = avgpp;
                return ret;

            if self.statuscost < k.c :
                self.statuscost = k.c;

        #if prek.vol > VOLTIMES * prevolume:
        #    print prek.c, prevalue, prek.c > prevalue, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(prek.t));
        # if (prek.c > prevalue and prek.vol > VOLTIMES * prevolume * dv) or (k.c > value and k.vol > VOLTIMES * volume * dv): #and k.c > phigh :#and k.vol < 3.5 * volume:
        closev = round((k.c - value)/value*100,2);
        if self.lastbuyidx != self.lastidx - 1 and summb >= 1 and closev > 1 and closev <= 10 and avgpp/closev > 0.5 and avgpp <= 10 and k.vol > VOLTIMES * volume * dv and self.statusdelay != self.lastidx: #and k.c > phigh :#and k.vol < 3.5 * volume:
        # if (k.c > value and k.vol > VOLTIMES * volume * dv and k.vol < 8 * VOLTIMES * volume * dv ) and self.statusdelay != self.lastidx: #and k.c > phigh :#and k.vol < 3.5 * volume:
            ret['type'] = 'buy'
            self.status = 'buy';
            ret['ext']['close'] = closev;
            ret['ext']['voltimes'] = round(k.vol / volume,2);
            ret['ext']['avgpp'] = avgpp;
            ret['ext']['ss'] = round(avgpp/closev, 2);
            if self.statusbuycurrent == 0:
                self.statuscost = k.c;
                self.statusbuycurrent = k.c;
                self.statusdelay = self.lastidx;
            else:
                self.statusdelay = self.lastidx + (self.lastidx - self.statusdelay) / 3;
            self.lastbuyidx = self.lastidx - 1;
            return  ret;

        return ret;
    def OrderResult(self, ret, orderresult):
        Log.d('\t\torder result, self status {0}, result type {1}, order result {2}'.format(self.status, ret['type'], orderresult));
        if ret['type'] == 'sell':
            if orderresult:
                self.status = 'sell';
                self.statuscost = 0;
                self.statusdelay = 0;
                self.statusbuycurrent = 0;

