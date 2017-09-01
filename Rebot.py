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
from Log import Log

class Rebot():

    def __init__(self, period):
        self.period = period;
        self.exchange = Exchange(RebotConfig.access_key, RebotConfig.secret_key);
        if RebotConfig.rebot_release:
            self.exchange.delegate(yunbiEX());
        else:
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
        self.markets = self.exchange.getMarkets();
        # rule.
        self.rules = {};
        # init.
        #
        #time and times;
        self.tradeSure = {}
        self.marketTime = {};
        for k,v in enumerate(self.markets):
            market = v['id'];
            # order.
            # done in right env.
            self.user.updateOrder(self.exchange.getOrder(market));
            # k line.
            if RebotConfig.rebot_is_test:
                dk = self.exchange.getK(market, 100, self.period, 1498838400); # 1498838400:2017/7/1 0:0:0; 1496246400:2017/6/1 0:0:0; 1493568000:2017/5/1 0:0:0
            else:
                dk = self.exchange.getK(market, 500, self.period);

            r = MutliMovingAverage();
            r.Run(dk);
            lastk=r.KLines.Get(-1);
            currency = market[0:len(market)-3];
            self.user.updateHigh(currency, lastk.c); # c or high
            self.user.updateCost(currency, lastk.c)

            self.rules[market] = r;
            self.tradeSure[market] = {'buy':0, 'sell':0};
            self.marketTime[market] = lastk.t;
            Log.d('start market:%s, begin time %s, current time:%s'%(market, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(r.KLines.Get(0).t)), time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(lastk.t))));
        #scale.
        self.scales = [];

    def run(self):
        # print '-----------------------------------------------------------------'
        # markets
        nmarkets = self.exchange.getMarkets()
        if nmarkets:
            self.markets = nmarkets;
        # user
        info = self.exchange.getUser();
        self.user.updatePositions(info['accounts']);
        if True:
            print 'positions:';
            for k,v in (self.user.positions.items()):
                if v['volume'] > 0:
                    print '{0} {1}'.format(k, v);
            # print '\n'

        sv  = self.user.positions['cny']['volume'];
        flag=False;
        buylist     = [];
        selllist    = [];
        for k,v in enumerate(self.markets):
            market = v['id'];
            # order.
            # done in right env.
            self.user.updateOrder(self.exchange.getOrder(market));
            # rule
            r = self.rules[market];
            lastk=r.KLines.Get(-1);
            # k line.
            # dk = self.exchange.getK(market, 500, self.period, lastk.t);
            dk = self.exchange.getK(market, 2, self.period, lastk.t);
            if dk and len(dk) > 0:
                ret     = r.Run(dk);
                lastk   = r.KLines.Get(-1);

                if self.marketTime[market] != lastk.t:
                    self.marketTime[market] = lastk.t;
                    self.tradeSure[market] = {'buy':0, 'sell':0};
                # print market, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.marketTime[market])), time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(lastk.t))
                type    = ret.get('type');
                if type == 'buy':
                    buylist.append({'market':market, 'result':ret})
                if type == 'sell':
                    selllist.append({'market':market, 'result':ret})
            print 'do market:{0}, market status : {1}, last k time : {2}'.format(market, r.status, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(lastk.t)));
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
                    rate = RebotConfig.rebot_loss_ratio;
                    if scale < rate:
                        if RebotConfig.rebot_is_test:
                            prate = (1 + rate * 1.1 / 100);
                            nprateprice = pc['price'] * prate;
                            vol = self.user.doOrder(market, 'sell', nprateprice);
                            print '\tmarket:%s, do sell, price:%f scale less %f, volume:%f, price:%f, time:%s' % (market, pc['price'], rate, vol, nprateprice, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(lastk.t)));

                            self.exchange.doOrder(market, 'sell', nprateprice, vol, lastk.t);
                        else:
                            selllist.append({'market':market, 'result':{'k':lastk, 'ext':'rebot loss ratio' }})
                    # else:
                    #    print '\tmarket:{0}, scale:{1}, position high price:{2}, current price{3}'.format(market, scale, pc['high'], lastk.c);
                cost = self.user.getHighCost(currency);
                if cost and cost > 0:
                    scale = (current - cost)/cost*100;
                    rate = RebotConfig.rebot_profit_ratio;
                    if scale < rate:
                        if RebotConfig.rebot_is_test:
                            prate = (1 + rate * 1.1 / 100);
                            nprateprice = pc['high'] * prate;
                            vol = self.user.doOrder(market, 'sell', nprateprice);
                            print '\tmarket:%s, do sell, high:%f scale less %f, volume:%f, high:%f, time:%s' % (market, pc['high'], rate, vol, nprateprice, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(lastk.t)));

                            self.exchange.doOrder(market, 'sell', nprateprice, vol, lastk.t);
                        else:
                            selllist.append({'market':market, 'result':{'k':lastk, 'ext':'rebot profit ratio' }})
                    # else:
                    # print '\tmarket:{0}, scale:{1}, position high price:{2}, current price{3}'.format(market, scale, pc['high'], lastk.c);
        # sell
        nselllist = [];
        for key,v in enumerate(selllist):
            market  = v['market'];
            self.tradeSure[market]['sell'] += 1;
            if self.tradeSure[market]['sell'] >= RebotConfig.rebot_trade_sure_times:
                nselllist.append(v);
        for key,v in enumerate(nselllist):
            market  = v['market'];
            k   = v['result']['k'];
            vol = self.user.doOrder(market, 'sell', k.c);
            if vol and vol > 0:
                Log.d('\tmarket:{0}, do:{1}, price:{2}, volume:{3} time:{4}, ext:{5}'.format(market, 'sell', k.c, vol, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(k.t)), v['result']['ext']));
                self.exchange.doOrder(market, 'sell', k.c, vol, k.t);

        # buy
        nbuylist = [];
        for k,v in enumerate(buylist):
            market = v['market'];
            sort = v['result']['sort'];
            v['sort'] = sort
            angle = v['result'].get('angle');
            k   = v['result']['k'];

            if sort > 100 or sort < 0:
                print '\tmarket %s sort illegal, sort %f, time %s' % (market, sort, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(k.t)));
                continue;
            if angle and angle < RebotConfig.rebot_buy_least_angle:
                print '\tmarket %s angle illegal, angle %f, time %s' % (market, angle, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(k.t)));
                continue;
            self.tradeSure[market]['buy'] += 1;
            if self.tradeSure[market]['buy'] >= RebotConfig.rebot_trade_sure_times:
                nbuylist.append(v);
            # nbuylist.append(v);

        nbuylist.sort(key=lambda v: v['sort'], reverse=False)
        for key,v in enumerate(nbuylist):
            market  = v['market'];
            k   = v['result']['k'];
            vol = self.user.doOrder(market, 'buy', k.c);
            self.exchange.doOrder(market, 'buy', k.c, vol, k.t, {'sort':v['sort']});
            flag=True;
            if vol > 0:
                Log.d('\tmarket:{0}, do:{1}, price:{2}, volume:{3}, time:{4}, ext:{5}'.format(market, 'buy', k.c, vol, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(k.t)), v['result']['ext']));
                self.tradeSure[market]['buy'] = -RebotConfig.rebot_do_per_period;
            #else:
            #    Log.d('\tnot enough cny !!! market:{0}, do:{1}, price:{2}, volume:{3}, time:{4}'.format(market, 'buy', k.c, vol, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(k.t))));
            #else:
            #    print '\t!!! market:{0}, time:{1}, buy fail less volume : {2}'.format(market, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(cwave.ck.t)), v['rmbvolumeN3']);
        if flag:
            ascale = (sv - self.user.initamount)/self.user.initamount*100;
            self.scales.append(ascale);
            Log.d('all scale:{0}, cuurent cny:{1}'.format(ascale, sv));


