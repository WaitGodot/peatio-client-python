
# order
# 
ORDERID = 0;

class OrderStatus():
    COMPELETE = 0; # 
    UNCOMPELETE = 1; # 
    REVOKED = 2; # 

class OrderType():
    BUY = 0;
    SELL = 1;

class Order():
    def __init__(self, type, market, time, price, count):
        ORDERID += 1;
        self.id = ORDERID;
        self.parent = ORDERID;
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