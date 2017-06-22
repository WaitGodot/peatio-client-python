
# order
# 
ORDERID = 0;

class OrderStatus():
    COMPELETE = 0; # 完成
    UNCOMPELETE = 1; # 未完成
    REVOKED = 2; # 撤销

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
    def 
    def Compelete(self, price, count):
        self.compeleteprice = price;
        self.leftcount = self.leftcount - count;
        if self.leftcount <= 0:
            self.status = OrderStatus.COMPELETE;
    def Revoked(self):
        if self.leftcount != self.count: