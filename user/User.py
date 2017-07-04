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
        self.amount = 0; # cash
        self.positions = {}; # 
        self.undone = {}; # 

    def buy(self, market, time, price, count):
        amount = price * count;
        if amount > self.amount:
            amount = self.amount;
            count = amount / price;
        if count <= 0 :
            print "not enough money!";

        o = Order(OrderType.BUY, market, time, price, count);
        self.undone[o.id] = o;
        self.amount = self.amount - amount;

        self.compeleteOrder(o); # only for test
        return o;

    def sell(self, market, time, price, count):
        pc = self.positions[market];
        if pc == None:
            print "not enough positions, market : {0}".format(market);
            return ;
        if pc < count:
            count = pc;
        o = Order(OrderType.SELL, market, time, price, count);
        self.undone[o.id] = o;

        self.compeleteOrder(o); # only for test
        return o;

    def compeleteOrder(self, id):
        o = self.undone[id]
        pc = self.positions[o.market];
        if pc == None:
            pc = 0;
        if o.type == OrderType.BUY:
            pc += o.count;
            self.positions[o.market] = pc;
        if o.type == OrderType.SELL:
            pc -= o.count;
            self.positions[o.market] = pc;

