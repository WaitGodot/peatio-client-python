
# order
# 
class OrderStatus():
    COMPELETE = 0; # 
    UNCOMPELETE = 1; # 
    REVOKED = 2; # 

class OrderType():
    BUY = 0;
    SELL = 1;

class Order():
    ORDERID = 0;
    def __init__(self, type, market, time, price, count):
        Order.ORDERID += 1;
        self.id = Order.ORDERID;
        self.parent = Order.ORDERID;
        self.type = type;
        self.market = market;
        self.time = time;
        self.userprice = price;
        self.count = count;
        self.leftcount = count;
        self.status = OrderStatus.UNCOMPELETE;
        self.compeleteprice = 0;

    def Compelete(self, price, count):
        self.compeleteprice = price;
        self.leftcount = self.leftcount - count;
        if self.leftcount <= 0:
            self.status = OrderStatus.COMPELETE;