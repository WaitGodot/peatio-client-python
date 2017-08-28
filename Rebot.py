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
from Time import Time

class Rebot():

    def __init__(self, period):
        self.period = period;
        self.exchange = Exchange(RebotConfig.access_key, RebotConfig.secret_key);
        # self.exchange.delegate(yunbiEX());
        self.exchange.delegate(yunbiEXLocal());
        # time
        Time.SetServerTime(self.exchange.getServerTimestamp())
        # user.
        self.user = User();
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
            dk = self.exchange.getK(market, 10, self.period, 1498838400); # 1498838400:2017/7/1 0:0:0; 1496246400:2017/6/1 0:0:0; 1493568000:2017/5/1 0:0:0
            r = MutliMovingAverage();
            r.Run(dk);
            self.rules[market] = r;
            self.buyTimes[market] = 0;
            self.sellTimes[market] = 0;
            lastk=r.KLines.Get(-1);
            print 'start market:%s, time:%s'  %(market, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(lastk.t)))
        #scale.
        self.scales = [];

    def run(self):
        # print '-----------------------------------------------------------------'
        # user
        info = self.exchange.getUser();
        self.user.updatePositions(info['accounts']);
        if False:
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
        summarketrmbvolume = 0;
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
                summarketrmbvolume += r.rmbvolumeN3;
                r.Run(dk);
                ret     = r.Do();
                lastk   = r.KLines.Get(-1);
                type    = ret.get('type');
                if type == 'buy':
                    buylist.append({'market':market, 'result':ret})
                if type == 'sell':
                    selllist.append({'market':market, 'result':ret})
                # position;
            currency = market[0:len(market)-3];
            pc = self.user.positions.get(currency);
            if pc and lastk:
                current = pc['volume'] * lastk.c;
                sv += current;

                self.user.updateHigh(currency, lastk.c); # c or high
                cost = self.user.getCost(currency);
                if cost and cost > 0:
                    scale = (current - cost)/cost*100;
                    rate = -10;
                    if scale < rate:
                        prate = (1 + rate * 1.1 / 100);
                        nprateprice = pc['price'] * prate;
                        vol = self.user.doOrder(market, 'sell', nprateprice);
                        self.exchange.doOrder(market, 'sell', nprateprice, vol, lastk.t);
                        print '\tmarket:%s, do sell, price:%f scale less %f, volume:%f, price:%f, time:%s' % (market, pc['price'], rate, vol, nprateprice, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(lastk.t)));
                    # else:
                    #    print '\tmarket:{0}, scale:{1}, position high price:{2}, current price{3}'.format(market, scale, pc['high'], lastk.c);
                cost = self.user.getHighCost(currency);
                if cost and cost > 0:
                    scale = (current - cost)/cost*100;
                    rate = -20;
                    if scale < rate:
                        prate = (1 + rate * 1.1 / 100);
                        nprateprice = pc['high'] * prate;
                        vol = self.user.doOrder(market, 'sell', nprateprice);
                        self.exchange.doOrder(market, 'sell', nprateprice, vol, lastk.t);
                        print '\tmarket:%s, do sell, high:%f scale less %f, volume:%f, high:%f, time:%s' % (market, pc['high'], rate, vol, nprateprice, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(lastk.t)));
                    # else:
                    # print '\tmarket:{0}, scale:{1}, position high price:{2}, current price{3}'.format(market, scale, pc['high'], lastk.c);
        # sell
        for k,v in enumerate(selllist):
            cwave   = v['result']['cwave'];
            market  = v['market'];
            vol = self.user.doOrder(market, cwave.type, cwave.cprice);
            self.exchange.doOrder(market, cwave.type, cwave.cprice, vol, cwave.ck.t);
            print '\tmarket:{0}, do:{1}, price:{2}, time:{3}'.format(market, cwave.type, cwave.cprice, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(cwave.ck.t)));

        # buy
        markets = {};
        marketsupdate.sort(key = lambda x : x[1], reverse=False);
        for k,v in enumerate(marketsupdate):
            if v[1] > 150000000 / 3:
                markets[v[0]] = True;
            markets[v[0]] = True;
            # print 'marketsupdate:', v[0], v[1], summarketrmbvolume/len(marketsupdate);

        nbuylist = [];
        for k,v in enumerate(buylist):
            market = v['market'];
            sort = v['result']['sort'];
            v['sort'] = sort
            print 'xxxx market:', market, 'sort:', sort;
            if sort > 100 or sort < 1:
                print '\tmarlet %s sort greater 10, sort %f' % (market, sort);
            else:
                nbuylist.append(v);
                print '123'
            # nbuylist.append(v);

        nbuylist.sort(key=lambda v: v['sort'], reverse=True)
        for k,v in enumerate(nbuylist):
            market  = v['market'];
            if markets.get(market):
                cwave   = v['result']['cwave'];
                vol = self.user.doOrder(market, cwave.type, cwave.cprice);
                self.exchange.doOrder(market, cwave.type, cwave.cprice, vol, cwave.ck.t, {'sort':v['sort']});
                flag=True;
                if vol > 0:
                    print '\tmarket:{0}, do:{1}, price:{2}, volume:{3}, time:{4}'.format(market, cwave.type, cwave.cprice, vol, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(cwave.ck.t)));
                else:
                    print '\tnot enough !!! market:{0}, do:{1}, price:{2}, volume:{3}, time:{4}'.format(market, cwave.type, cwave.cprice, vol, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(cwave.ck.t)));
            #else:
            #    print '\t!!! market:{0}, time:{1}, buy fail less volume : {2}'.format(market, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(cwave.ck.t)), v['rmbvolumeN3']);
        if flag:
            ascale = (sv - self.user.initamount)/self.user.initamount*100;
            self.scales.append(ascale);
            print 'all scale:{0}'.format(ascale);
        '''
        print 'positions:';
        for k,v in (self.user.positions.items()):
            if v['volume'] > 0:
                print '\t{0} {1}'.format(k, v);
        '''

