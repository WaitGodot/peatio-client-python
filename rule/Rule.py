# rule
from lib.client import Client, get_api_path
from formula.K import KLine
from formula.MACD import MACD
from formula.KDJ import KDJ
from formula.Formula import CROSS
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
        self.WaveMACD_DIFF = WavePoint();
        self.WaveMACD_DEA = WavePoint();
        self.WaveMACD_MACD = WavePoint();
        self.WaveKDJ_K = WavePoint();
        self.WaveKDJ_D = WavePoint();

        self.client = Client(access_key=BotConfig.access_key, secret_key=BotConfig.secret_key)
        self.begin = 0;

    def Run(self):
        d = self.client.get(get_api_path('k'), params={'market': '{0}cny'.format(self.market), 'limit':1000,'period' : '{0}'.format(self.period)});
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(d[0][0]));
        self.KLines.Input(d);
        self.MACD.Input(self.KLines);
        self.KDJ.Input(self.KLines);

        self.WaveKline.Input(self.KLines);
        self.WaveMACD_DIFF.Input(self.MACD.DIFF);
        self.WaveMACD_DEA.Input(self.MACD.DEA)
        self.WaveKDJ_K.Input(self.KDJ.K);
        self.WaveKDJ_D.Input(self.KDJ.D);
        klen = len(self.KLines);
        self.begin  = klen;

    def Trend(self): # macd diff, dea 0 de daxiao
        lmacd = len(self.MACD);
        if lmacd < 2:
            return Direction.FLAT;
        if self.MACD.DIFF[len-1] >= 0 and self.MACD.DIFF[len-2] >= 0 and self.MACD.DEA[len-1] >= 0 and self.MACD.DEA[len-2] >=0:
            return Direction.UP:
        return Direction.DOWN;
    #macd diff current value, 
    def MACD_DIFF(self):
        c = self.WaveMACD_DIFF.Get(-1);
        pc = self.WaveMACD_DIFF.Get(-2, c.dir);
        
        
