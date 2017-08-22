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
        # 
        self.buyTimes = {};
        self.sellTimes = {};
        for k,v in enumerate(self.markets):
            market = v['id'];
            # order.
            # done in right env.
            self.user.updateOrder(self.exchange.getOrder(market));
            # k line.
            # dk = self.exchange.getK(market, 500, self.period);
            dk = self.exchange.getK(market, 10, self.period, 1498838400); # 1498838400:2017/7/1 0:0:0
            r = MutliMovingAverage();
            r.Run(dk);
            self.rules[market] = r;
            self.buyTimes[market] = 0;
            self.sellTimes[market] = 0;
        #
        
    def run(self):
        print '-----------------------------------------------------------------'
        # user
        info = self.exchange.getUser();
        self.user.updatePositions(info['accounts']);
        print 'positions:', self.user.positions;
        
        # sever timestamp
        # t = self.exchange.getServerTimestamp();
        # markets
        sv = self.user.positions['cny']['volume'];
        for k,v in enumerate(self.markets):
            market = v['id'];
            print 'do marekt:{0}'.format(market);
            # order.
            # done in right env.
            self.user.updateOrder(self.exchange.getOrder(market));
            # rule
            r = self.rules[market];
            lastk=r.KLines.Get(-1);
            # k line.
            # dk = self.exchange.getK(market, 500, self.period, lastk.t);
            dk = self.exchange.getK(market, 2, self.period, lastk.t);
            if dk:
                r.Run(dk);
                ret=r.Do();
                lastk=r.KLines.Get(-1);
                if ret:
                    print 'market:{0}, do:{1}, price:{2}'.format(market, ret, lastk.c);
                    vol = self.user.doOrder(market, ret, lastk.c);
                    self.exchange.doOrder(market, ret, lastk.c, vol, lastk.t);
            # position;
            currency = market[0:len(market)-3];
            pc = self.user.positions.get(currency);
            if pc and lastk:
                cost = self.user.getCost(currency);
                current = pc['volume'] * lastk.c;
                sv += current;
                if cost and cost > 0:
                    scale = (current - cost)/cost*100;
                    if scale<-7.7:
                        vol = self.user.doOrder(market, 'sell', pc['price'] * 0.9);
                        self.exchange.doOrder(market, 'sell', pc['price'] * 0.9, vol);
                        print 'do sell, scale less 0.077!!';
                    print '\tmarket:{0}, scale:{1}, position price:{2}, current price{3}'.format(market, scale, pc['price'], lastk.c);

        print 'all scale:{0}'.format((sv - self.user.initamount)/self.user.initamount*100)

