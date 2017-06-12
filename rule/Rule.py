# rule
from lib.client import Client, get_api_path
from formula.K import KLine
from formula.MACD import MACD
from BotConfig import BotConfig
from rule.WaveKline import WaveKline
from rule.WavePoint import WavePoint

import time;

class Rule():
    def __init__(self, market, period):
    	self.market = market;
        self.period = period;
        self.KLines = KLine();
        self.MACD = MACD();
        self.WaveKline = WaveKline();
        self.WavePoint = WavePoint();

        self.client = Client(access_key=BotConfig.access_key, secret_key=BotConfig.secret_key)

    def Run(self):
        d = self.client.get(get_api_path('k'), params={'market': '{0}cny'.format(self.market), 'period' : '{0}'.format(self.period)});
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(d[0][0]));
        self.KLines.Input(d);
        self.MACD.Input(self.KLines);
        self.WaveKline.Input(self.KLines);
        self.WavePoint.Input(self.MACD.DIFFS);

        print self.WavePoint;
