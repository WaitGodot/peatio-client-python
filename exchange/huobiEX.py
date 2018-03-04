from RebotConfig import RebotConfig
from Log import Log
from exchange.huobi.HuobiUtil import *
from exchange.huobi.HuobiService import *
import json
import time
import math

'''{1min, 5min, 15min, 30min, 60min, 1day, 1mon, 1week, 1year }'''
PERIOD2TYPE = {
    1   :   '1min',
    5   :   '5min',
    15  :   '15min',
    30  :   '30min',
    60  :   '60min',
    240 :   '1day',
    1680:   '1week',
}

def PERIOD(period):
    return PERIOD2TYPE.get(period);
def TIMESTAMP(period, timestamp):
    st=None;
    if period >= 240:
        st = time.strftime("%Y-%m-%d", time.localtime(timestamp));
    else:
        st = time.strftime("%Y-%m-%d %H:%M", time.localtime(timestamp));
    return st;
class huobiEX():

    def set(self, access, secret):
        set_user_key(access, secret);
    # function
    def loadData(self, period, timestamp):
        return None;

    def prepare(self, period, timestamp):
        return None;

    def getServerTimestamp(self):
        return time.time();

    def getUser(self):
        return None;

    def getMarkets(self):
        if  len(RebotConfig.rebot_trade_markets) > 0:
            return RebotConfig.rebot_trade_markets;
        return [];

    def getK(self, market, limit, period, timestamp=None):
        data = get_kline(market, PERIOD(period), limit);
        ndata = [];
        for k,v in enumerate(data):
            d = [];
            d[0] = v['id'];
            d[1] = v['open'];
            d[2] = v['high'];
            d[3] = v['low'];
            d[4] = v['close'];
            d[5] = v['vol'];
            ndata.append(d);

        return ndata;

    def getOrder(self, market):
        return None;

    def doOrder(self, market, side, price, volume, time=None, ext=None):
        return None;

    def doOrderCancel(self, orderID, market):
        return None;


class huobiEXLocal():

    def set(self, access, secret):
        set_user_key(access, secret)
        self.accounts = {
            'usdt' : {'currency':'usdt', 'balance':'%d' % RebotConfig.user_initamount, 'locked':'0.0'},
        };
        self.orders = {};
        self.marketOrders = {};
        self.ORDERID = 0;
        self.kss = {};
        self.allMarkets = None;
        self.currentMarkets = None;
        self.poundage = 0;#0.0001;

    def createOrder(self, market, side, time, price, volume, ext):
        volume = math.floor(volume/100)*100;
        if volume<=0:
            return None;
        self.ORDERID += 1;
        id = self.ORDERID;
        o = {
            'id':id,
            'side':side, # sell, buy
            'price':price,
            'avg_price':price,
            'state':'wait', # wait, done, cancel
            'market':market,
            'created_at':time,
            'volume':volume,
            'remaining_volume':volume,
            'executed_volume':0,
            'ext':ext
        }
        self.orders[id] = o;
        d = self.marketOrders.get(market);
        if d==None:
            self.marketOrders[market] = [];
            d = self.marketOrders.get(market);
        d.append(o);
        return id;

    def compeleteOrder(self, id):
        o = self.orders.get(id);
        if o==None:
            return;
        market = o['market'];
        currency = market;#market[0:len(market)-3];

        o['remaining_volume']=0;
        o['executed_volume']=o['volume'];
        o['state']='done';

        if o['side'] == 'sell':
            c = self.accounts.get(currency);
            balance = float(c['balance']);
            c['balance'] = str(balance - o['executed_volume']);
            ccny = self.accounts.get('cny');
            ccny['balance'] = str(float(ccny['balance']) + o['executed_volume'] * o['avg_price'] * (1 - self.poundage) );
            print '\t\tsell', market, balance, c['balance']
        if o['side'] == 'buy':
            c = self.accounts.get(currency);
            if c==None:
                self.accounts[currency] = {'currency':currency, 'balance':'0.0', 'locked':'0.0', 'price':0.0};
                c = self.accounts.get(currency);
            balance = float(c['balance']);
            price = c['price'];
            addbalance = o['executed_volume'] * (1 - self.poundage);
            addprice = o['avg_price'];

            print '\t\tbuy',market, balance, addbalance
            c['balance'] = str(balance + addbalance);
            c['price'] = (balance)/(balance+addbalance)*price + addbalance/(balance+addbalance)*addprice;

            ccny = self.accounts.get('cny');
            ccny['balance'] = str(float(ccny['balance']) - addbalance*addprice);


    # function
    def loadData(self, period, timestamp):
        return None;

    def prepare(self, period, timestamp):
        return None;

    def getServerTimestamp(self):
        return time.time();
        
    def getUser(self):
        d = {}
        accounts = [];
        for k,v in self.accounts.items():
            accounts.append(v);
        d['accounts']=accounts;
        return d;

    def getMarkets(self):
        if  len(RebotConfig.rebot_trade_markets) > 0:
            return RebotConfig.rebot_trade_markets;

        data = get_symbols();
        return data;
        #return [{'id':'anscny'},{'id':'btccny'}, {'id':'ethcny'}, {'id':'zeccny'}, {'id':'qtumcny'}, {'id':'gxscny'}, {'id':'eoscny'}, {'id':'sccny'}, {'id':'dgdcny'}, {'id':'1stcny'}, {'id':'btscny'}, {'id':'gntcny'}, {'id':'repcny'}, {'id':'etccny'}];
        #return [{'id':'anscny'}];

    def getK(self, market, limit, period, timestamp=None):
        ks = self.kss.get(market);
        if ks==None:
            data = get_kline(market, PERIOD(period), 2000);
            datadata = data['data'];
            ndata = [];
            lendatadata = len(datadata);
            for k in range(0, lendatadata):
                v = datadata[lendatadata - 1 - k];
                if v['id'] >= timestamp:
                    d = [0,1,2,3,4,5];
                    d[0] = v['id'];
                    d[1] = v['open'];
                    d[2] = v['high'];
                    d[3] = v['low'];
                    d[4] = v['close'];
                    d[5] = v['vol'];
                    ndata.append(d);
            
            self.kss[market] = ndata;
            ks = self.kss.get(market);
            # time.sleep(0.01);
        if ks == None or len(ks) == 0:
            print '%s do not find kline' % market
        if timestamp > ks[-1][0]:
            print '{0} k line is over'.format(market);
            return [];
        ret = [];
        for k,v in enumerate(ks):
            if v[0] >= timestamp:
                ret.append(v);
            if len(ret) >= limit:
                return ret;
        return ret;

    def getOrder(self, market):
        ret = self.marketOrders.get(market);
        if ret==None:
            return [];
        return ret;

    def doOrder(self, market, side, price, volume, time=None, ext=None):
        id = self.createOrder(market, side, time, price, volume, ext)
        if id:
            self.compeleteOrder(id);

    def doOrderCancel(self, orderID):
        return None;
