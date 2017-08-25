
class Exchange():

    def __init__(self, access, sercet):
        self.access = access;
        self.sercet = sercet;

    def delegate(self, delegate):
        delegate.set(self.access, self.sercet);
        self.delegate = delegate;

    # function .
    def getServerTimestamp(self):
        if self.delegate:
            return self.delegate.getServerTimestamp();
        return None;
    def getUser(self):
        if self.delegate:
            return self.delegate.getUser();
        return None;

    def getMarkets(self):
        if self.delegate:
            return self.delegate.getMarkets();
        return None;

    def getK(self, market, limit, period, timestamp=None):
        if self.delegate:
            return self.delegate.getK(market, limit, period, timestamp);
        return None;

    def getOrder(self, market):
        if self.delegate:
            return self.delegate.getOrder(market);
        return None;

    def doOrder(self, market, side, price, vol, time=None, ext=None):
        if self.delegate:
            return self.delegate.doOrder(market, side, price, vol, time, ext);
        return None;

    def doOrderCancel(self, orderID):
        if self.delegate:
            return self.delegate.doOrderCancel(orderID);
        return None;
        
