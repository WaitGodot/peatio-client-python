
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

class WVStats():
    def __init__(self, ValueN=10):
        self.KLines = KLine();
        self.Value = [];
        self.Volume = [];
        self.ValueN = ValueN;
        self.status = None;
        self.statusdelay = 0;
        self.stats = [];

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
        self.KLines.Input(d);

        MA(self.KLines.prices, self.Value, self.ValueN);
        MA(self.KLines.volumes, self.Volume, self.ValueN);

        return self.Do();

    def Do(self, idx=-1, ignore=False):
        k = self.KLines.Get(idx);
        value = self.Value[idx];
        volume = self.Volume[idx];
        ret = {};

        ret['type'] = None;
        ret['k']    = k;
        ret['sort'] = 1;
        ret['angle'] = 10;
        ret['ext'] = {'idx':idx}

        statslen = len(self.stats)
        for i in range(0, statslen):
            nk = statslen - i - 1;
            arr = self.stats[nk];
            if len(arr) < 5:
                arr.append({'k':k, 'value':value, 'volume':volume});

        if k.c > value and k.vol > 2 * volume:
            ret['type'] = 'buy'
            self.status = 'buy';
            self.statusdelay = 0;
            self.stats.append([]);
            return  ret;

        if self.status == 'buy':
            self.statusdelay = self.statusdelay + 1;
            if self.statusdelay >= 5 :
                ret['type'] = 'sell';
                self.status = 'sell';
                self.statusdelay = 0;
                return ret;

        return ret;