
from exchange.yunbi.client import Client, get_api_path

import json

class yunbiEX():
    
    def set(self, access, sercet):
        self.client = Client(access_key=access, secret_key=sercet);

    # function 
    def getServerTimestamp(self):
        return self.client.get(get_api_path('timestamp'));

    def getUser(self):
        return self.client.get(get_api_path('members'));

    def getMarkets(self):
        return self.client.get(get_api_path('markets'));

    def getK(self, market, limit, period, timestamp=None):
        if timestamp==None:
            return self.client.get(get_api_path('k'), params={'market': market, 'limit':'{0}'.format(limit),'period':'{0}'.format(period)});
        else:
            return self.client.get(get_api_path('k'), params={'market': market, 'limit':'{0}'.format(limit),'period':'{0}'.format(period), 'timestamp':'{0}'.format(timestamp)});
    	return None

    def getOrder(self, market):
    	return self.client.get(get_api_path('orders'), {'market': market});

    def doOrder(self, market, side, price, vol):
        return self.client.post(get_api_path('orders'), params = {'market':market, 'side':side, 'price':price, 'volume':vol})

    def doOrderCancel(self, orderID):
        return self.client.post(get_api_path('delete_order'), params ={'id':orderID});

class yunbiEXLocal():
    
    def set(self, access, sercet):
        self.client = Client(access_key=access, secret_key=sercet);
        self.accounts = {
            'cny' : {'currency':'cny', 'balance':'10000', 'locked':'0.0'},
        };
        self.orders = {};
        self.marketOrders = {};
        self.ORDERID = 0;
        self.kss = {};
    
    def createOrder(self, market, side, time, price, volume):
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
        currency = market[0:len(market)-3];

        o['remaining_volume']=0;
        o['executed_volume']=o['volume'];
        o['state']='done';

        if o['side'] == 'sell':
            c = self.accounts.get(currency);
            balance = float(c['balance']);
            c['balance'] = str(balance - o['executed_volume']);
            ccny = self.accounts.get('cny');
            ccny['balance'] = str(float(ccny['balance']) + o['executed_volume'] * o['avg_price'] );
        if o['side'] == 'buy':
            c = self.accounts.get(currency);
            if c==None:
                self.accounts[currency] = {'currency':currency, 'balance':'0.0', 'locked':'0.0', 'price':0.0};
                c = self.accounts.get(currency);
            balance = float(c['balance']);
            price = c['price'];
            addbalance = o['executed_volume'];
            addprice = o['avg_price'];

            c['balance'] = str(balance + addbalance);
            c['price'] = (balance)/(balance+addbalance)*price + addbalance/(balance+addbalance)*addprice;

            ccny = self.accounts.get('cny');
            ccny['balance'] = str(float(ccny['balance']) - addbalance*addprice);


    # function 
    def getServerTimestamp(self):
        return self.client.get(get_api_path('timestamp'));

    def getUser(self):
        d = {}
        accounts = [];
        for k,v in self.accounts.items():
            accounts.append(v);
        d['accounts']=accounts;
        return d;

    def getMarkets(self):
        # return self.client.get(get_api_path('markets'));
        return [{'id':'etccny'}];

    def getK(self, market, limit, period, timestamp=None):
        ks = self.kss.get(market);
        if ks==None:
            ks = self.client.get(get_api_path('k'), params={'market': market, 'limit':4000,'period':period, 'timestamp':timestamp});
            self.kss[market] = ks;
        if timestamp > ks[-1][0]:
            print '{0} k line is over'.format(market);
            return None;
        ret = [];
        for k,v in enumerate(ks):
            if v[0] >= timestamp:
                ret.append(v);
            if len(ret) >= limit:
                return ret;

    def getOrder(self, market):
        ret = self.marketOrders.get(market);
        if ret==None:
            return [];
        return ret;

    def doOrder(self, market, side, price, volume):
        id = self.createOrder(market, side, 1, price, volume)
        if id:
            self.compeleteOrder(id);

    def doOrderCancel(self, orderID):
        return self.client.post(get_api_path('delete_order'), params ={'id':orderID});
