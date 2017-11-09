import tushare as ts
import time

class Client():
    def __init__(self, access_key=None, secret_key=None):
        self.access_key = access_key;
        self.secret_key = secret_key;

    def time(self):
        return time.time();

    def getK(self, market, period, timestamp):
        return ts.get_k_data(market, start = timestamp, ktype = period);

    def getMarkets(self):
        data = ts.get_today_all();
        

print ts.get_today_all();
