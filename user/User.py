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
        self.amount = 10000; # cash
        self.preamount = self.amount;
        self.svamount = self.amount;
        self.positions = {}; # [market]=count
        self.orders = {};
        self.tradetimes = 0;
        self.wintimes = 0;
    
    def updatePositions(self, positions):
        for key, value in enumerate(positions):
            self.positions[value['currency']] = float(value['balance']) - float(value['locked']);
            # if self.positions[value['currency']] > 0:
            #    print value;
    def updateOrder(self, orders):
        # id, type, market, time, price, volume
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

            o = self.orders.get(id);
            if o:
                if state == 'cancel':
                    o.update(averageprice, leftvolume, 'cancel');
                else:
                    o.update(averageprice, leftvolume);
            else:
                o = Order(id, type, market, t, price, volume);
                self.orders[id] = o;


    def buy(self, market, time, price, volume=None):
        if volume==None:
            volume = self.amount / price;
        amount = price * volume;
        if amount > self.amount:
            amount = self.amount;
            volume = amount / price;
        if volume < 1 :
            print "not enough money!";
            return 0;
        return volume;

    def sell(self, market, time, price, volume=None):
        pc = self.positions.get(market);
        if pc == None:
            print "not enough positions, market : {0}".format(market);
            return 0;
        if volume==None:
            volume = pc;
        if pc < volume:
            volume = pc;

        if volume < 1:
            return 0;
        return volume;

    def updateOrderWithID(self, id):
        o = self.orders[id]
        o.update(o.userprice, 0);
        self.tradetimes += 1;
        pc = self.positions.get(o.market);
        
        if pc == None:
            pc = 0;
        if o.type == "buy":
            self.positions[o.market] = pc + o.volume;
            self.preamount = self.amount;
            self.amount = self.amount - o.averageprice * o.volume;
            print 'buy complete price:{0}'.format(o.averageprice);
        if o.type == "sell":
            self.positions[o.market] = pc - o.volume;
            self.amount = self.amount + o.averageprice * o.volume;
            if self.amount > self.preamount:
                self.wintimes += 1;
            print 'sell complete price:{0}, amount:{1}, order:{2}%, all:{3}%, win:{4}'.format(o.averageprice, self.amount, 100*(self.amount-self.preamount)/self.preamount, 100*(self.amount-self.svamount)/self.svamount, self.wintimes/float(self.tradetimes));
            print '--------------------------------------------------------------------------------------------------'

