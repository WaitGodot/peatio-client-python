import time
import urllib2

from exchange.Exchange import Exchange
from exchange.yunbiEX import yunbiEX
from exchange.yunbiEX import yunbiEXLocal

from formula.K import KLine
from formula.MACD import MACD
from formula.Formula import SMA
from formula.Formula import MA
from formula.Formula import EMA
from formula.Formula import HIGH
from formula.Formula import LOW
from RebotConfig import RebotConfig
from rule.Rule import Rule
from rule.MutliMovingAverage import MutliMovingAverage
from user.User import User

class Rebot():

    def __init__(self, period):
        self.period = period;
        self.exchange = Exchange(RebotConfig.access_key, RebotConfig.secret_key);
        # self.exchange.delegate(yunbiEX());
        self.exchange.delegate(yunbiEXLocal());
        self.user = User();
        # user.
        info = self.exchange.getUser();
        print info
        print '-----------------------------------'
        self.user.updatePositions(info['accounts']);
        # markets
        print '-----------------------------------'
        self.markets = self.exchange.getMarkets();
        print self.markets
        print '-----------------------------------'
        # rule.
        self.rules = {}; #MutliMovingAverage();
        # init.
        for k,v in enumerate(self.markets):
            m = v['id'];
            # order.
            # done in right env.
            self.user.updateOrder(self.exchange.getOrder(m));
            # k line.
            dk = self.exchange.getK(m, 500, self.period);
            r = MutliMovingAverage();
            r.Run(dk);
            self.rules[m] = r;
        
    def run(self):
        # user
        info = self.exchange.getUser();
        self.user.updatePositions(info['accounts']);
        # markets
        for k,v in enumerate(self.markets):
            m = v['id'];
            # order.
            # done in right env.
            self.user.updateOrder(self.exchange.getOrder(m));
            # rule
            r = self.rules[m];
            lastk = r.KLines.Get(-1);
            # k line.
            dk = self.exchange.getK(m, 500, self.period, lastk.t);
            
            r.Run(dk);
            ret=r.Do();
            if ret:
                print 'market:{0}, do:{1}'.format(m, ret);

