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
        # print '-----------------------------------------------------------------'
        # user
        info = self.exchange.getUser();
        self.user.updatePositions(info['accounts']);
        print 'positions:';
        for k,v in (self.user.positions.items()):
            if v['volume'] > 0:
                print '\t{0} {1}'.format(k, v);
        
        # sever timestamp
        # t = self.exchange.getServerTimestamp();
        # markets
        sv  = self.user.positions['cny']['volume'];
        flag=False;
        buylist     = [];
        selllist    = [];
        mustselllist= [];

        marketsupdate = [];
        for k,v in enumerate(self.markets):
            market = v['id'];
            # order.
            # done in right env.
            self.user.updateOrder(self.exchange.getOrder(market));
            # rule
            r = self.rules[market];
            lastk=r.KLines.Get(-1);
            # print 'do marekt:{0}, current price:{1}'.format(market, lastk.c);
            # k line.
            # dk = self.exchange.getK(market, 500, self.period, lastk.t);
            dk = self.exchange.getK(market, 2, self.period, lastk.t);
            if dk:
                marketsupdate.append([market, r.rmbvolumeN3])
                r.Run(dk);
                ret     = r.Do();
                lastk   = r.KLines.Get(-1);
                type    = ret.get('type');
                if type == 'buy':
                    buylist.append({'market':market, 'result':ret})
                    flag=True;
                if type == 'sell':
                    selllist.append({'market':market, 'result':ret})
                    flag=True;
                # position;
                currency = market[0:len(market)-3];
                pc = self.user.positions.get(currency);
                if pc and lastk:
                    cost = self.user.getCost(currency);
                    current = pc['volume'] * lastk.c;
                    sv += current;
                    #if cost and cost > 0:
                    #    scale = (current - cost)/cost*100;
                    #    if scale<-15:
                    #        vol = self.user.doOrder(market, 'sell', pc['price'] * 0.85);
                    #        self.exchange.doOrder(market, 'sell', pc['price'] * 0.85, vol);
                    #        print 'do sell, scale less 0.077!!';
                    #    print '\tmarket:{0}, scale:{1}, position price:{2}, current price{3}'.format(market, scale, pc['price'], lastk.c);
        # sell
        for k,v in enumerate(selllist):
            cwave   = v['result']['cwave'];
            market  = v['market'];
            vol = self.user.doOrder(market, cwave.type, cwave.cprice);
            self.exchange.doOrder(market, cwave.type, cwave.cprice, vol, cwave.ck.t);
            print '\tmarket:{0}, do:{1}, price:{2}, time:{3}'.format(market, cwave.type, cwave.cprice, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(cwave.ck.t)));

        # buy
        markets = {};
        marketsupdate.sort(key = lambda x : x[1], reverse=True);
        for k,v in enumerate(marketsupdate):
            if k > 6:
                break;
            markets[v[0]] = True;
            print 'marketsupdate:', v[0], v[1];

        nbuylist = [];
        for k,v in enumerate(buylist):
            cwave   = v['result']['cwave'];
            market  = v['market'];
            v['rmbvolumeN3'] = self.rules[market].rmbvolumeN3;
            if cwave.crmbvolume > 600000 and cwave.crmbvolume < 10000000:
                v['sort'] = 1 + cwave.crmbvolume / 10000000;
                nbuylist.append(v);
            if cwave.crmbvolume > 10000000 and cwave.crmbvolume < 25000000:
                v['sort'] = 2 + cwave.crmbvolume / 25000000;
                nbuylist.append(v);

        nbuylist.sort(key=lambda v: v['sort'], reverse=False)
        for k,v in enumerate(nbuylist):
            market  = v['market'];
            if markets.get(market):
                cwave   = v['result']['cwave'];
                vol = self.user.doOrder(market, cwave.type, cwave.cprice);
                self.exchange.doOrder(market, cwave.type, cwave.cprice, vol, cwave.ck.t);
                print '\tmarket:{0}, do:{1}, price:{2}, rmb volume:{3}, time:{4}'.format(market, cwave.type, cwave.cprice, cwave.crmbvolume, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(cwave.ck.t)));
            else:
                print '\t!!! market:{0}, time:{1}, buy fail less volume'.format(market, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(cwave.ck.t)));
        if flag:
            print 'all scale:{0}'.format((sv - self.user.initamount)/self.user.initamount*100)
            print '---------------------------------------------------------------------------'

