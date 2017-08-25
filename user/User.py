# user
#
#
from user.Order import Order

class User():
    instanse = None;
    def Instanse():
        if User.instanse == None:
        	user.instanse = User();
        return user.instanse;

    def __init__(self):
        self.amount = 0; # cash
        self.initamount = 10000;
        self.positions = {}; # [market]=count
        self.orders = {};
        self.tradetimes = 0;
        self.wintimes = 0;
    
    def getAllCost(self):
        s = 0
        for key, value in(self.positions.items()):
            s += value['volume'] * value['price'];
        return s;

    def getCost(self, market):
        pc = self.positions[market];
        if pc==None:
            return None;
        return pc['volume'] * pc['price'];

    def getOrderMarket(self, market):
        d = [];
        for k,v in(self.orders.items()):
            if v.market == market:
                d.append(v);
        return d;
        
    def updatePositions(self, positions):
        for key, value in enumerate(positions):
            vol = float(value['balance']) - float(value['locked']);
            price = value.get('price');
            currency = value['currency'];
            pc = self.positions.get(currency);
            if pc==None:
                self.positions[currency] = {'volume':0, 'price':1}; # default.
                pc = self.positions[currency];
            if price!=None:
                pc['price'] = price;
            pc['volume']=vol;
            if currency=='cny':
                self.amount = vol;

    def updateOrder(self, orders):
        for key, value in enumerate(orders):
            id   = value['id'];
            type = value['side'];
            market = value['market'];
            t = value['created_at'];
            price = value['price'];
            volume = value['volume'];
            averageprice = value['avg_price'];
            leftvolume = value['remaining_volume'];
            state = value['state'];
            ext = value.get('ext');

            o = self.orders.get(id);
            if o:
                if state == 'cancel':
                    o.update(averageprice, leftvolume, 'cancel');
                else:
                    o.update(averageprice, leftvolume);
            else:
                o = Order(id, type, market, t, price, volume, ext);
                self.orders[id] = o;

    def doOrder(self, market, side, price, volume=None):
        if side == 'buy':
            if volume==None:
                if self.amount < 1000:
                    volume = self.amount / price;
                else:
                    volume = self.amount / price / 3;
            amount = price * volume;
            if amount > self.amount:
                amount = self.amount;
                volume = amount / price;
            self.amount = self.amount - amount;
            return volume;
        if side == 'sell':
            currency = market[0:len(market)-3];
            pc = self.positions.get(currency);
            if pc==None:
                return;
            v = pc['volume'];
            if pc == None or v <= 0:
                print "not enough positions, market : {0}".format(currency);
                return 0;
            if volume==None:
                volume = v;
            if v < volume:
                volume = v;
            return volume;

