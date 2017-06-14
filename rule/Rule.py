# rule
from lib.client import Client, get_api_path
from formula.K import KLine
from formula.MACD import MACD
from formula.KDJ import KDJ
from BotConfig import BotConfig
from rule.WaveKline import WaveKline
from rule.WavePoint import WavePoint
from rule.WaveKline import Direction

import time;

class Rule():
    def __init__(self, market, period):
        self.market = market;
        self.period = period;
        self.KLines = KLine();
        self.MACD = MACD();
        self.KDJ = KDJ();
        self.WaveKline = WaveKline();
        self.WaveKDJ_K = WavePoint();

        self.client = Client(access_key=BotConfig.access_key, secret_key=BotConfig.secret_key)
        self.begin = 0;

    def Run(self):
        d = self.client.get(get_api_path('k'), params={'market': '{0}cny'.format(self.market), 'limit':1000,'period' : '{0}'.format(self.period)});
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(d[0][0]));
        self.KLines.Input(d);
        self.MACD.Input(self.KLines);
        self.KDJ.Input(self.KLines);
        # self.KDJ.Export('c:\\Users\\randy\\k.csv');

        self.WaveKline.Input(self.KLines);
        self.WaveKDJ_K.Input(self.KDJ.K);
        # self.WaveKDJ_K.Export('c:\\Users\\randy\\wave.csv');
        klen = len(self.KLines);
        for idx in range(self.begin, klen):
            # buy 
            kseg1 = self.WaveKline.Get(-1); # k,kd,ku
            kmacd1 = self.MACD.Get(-1);
            kkdj1 = self.KDJ.Get(-1);
            if kseg1.dir == Direction.DOWN:
                kdseg2 = self.WaveKline.Get(-2, Direction.DOWN);
                if kseg1.lk.l < kdseg2.lk.l: # low low
                    # macd 
                    kmacd2 = self.MACD.Get(kdseg2.lkidx);
                    # kdj
                    kkdj2 = self.KDJ.Get(kdseg2.lkidx);
                    if kmacd2.diff < 0 and kmacd2.dea < 0 and kmacd1 > kmacd2 and kkdj1.k > kkdj2.k:
                        print 'buy idx :'.format(idx);
            # sell



        self.begin  = klen;

