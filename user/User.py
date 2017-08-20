# user
#
#
from user.Order import Order
from user.Order import OrderType

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
        self.undone = {}; # 
        self.tradetimes = 0;
        self.wintimes = 0;

    def buy(self, market, time, price, count=None):
        if count==None:
            count = self.amount / price;
        amount = price * count;
        if amount > self.amount:
            amount = self.amount;
            count = amount / price;
        if count <= 0 :
            print "not enough money!";
        
        if count < 1:
            return ;
        o = Order(OrderType.BUY, market, time, price, count);
        self.undone[o.id] = o;

        self.compeleteOrder(o.id); # only for test
        return o;

    def sell(self, market, time, price, count=None):
        pc = self.positions.get(market);
        if pc == None:
            print "not enough positions, market : {0}".format(market);
            return ;
        if count==None:
            count = pc;
        if pc < count:
            count = pc;

        if count < 1:
            return ;
        o = Order(OrderType.SELL, market, time, price, count);
        self.undone[o.id] = o;

        self.compeleteOrder(o.id); # only for test
        return o;

    def compeleteOrder(self, id):
        o = self.undone[id]
        o.Compelete(o.userprice, o.leftcount);
        self.tradetimes += 1;
        pc = self.positions.get(o.market);
        
        if pc == None:
            pc = 0;
        if o.type == OrderType.BUY:
            self.positions[o.market] = pc + o.count;
            self.preamount = self.amount;
            self.amount = self.amount - o.compeleteprice * o.count;
            print 'buy complete price:{0}'.format(o.compeleteprice);
        if o.type == OrderType.SELL:
            self.positions[o.market] = pc - o.count;
            self.amount = self.amount + o.compeleteprice * o.count;
            if self.amount > self.preamount:
                self.wintimes += 1;
            print 'sell complete price:{0}, amount:{1}, order:{2}%, all:{3}%, win:{4}'.format(o.compeleteprice, self.amount, 100*(self.amount-self.preamount)/self.preamount, 100*(self.amount-self.svamount)/self.svamount, self.wintimes/float(self.tradetimes));
            print '--------------------------------------------------------------------------------------------------'

