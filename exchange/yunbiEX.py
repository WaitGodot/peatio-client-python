
from exchange.yunbi.client import Client, get_api_path

class yunbiEX():

    def set(self, access, sercet):
        self.client = Client(access_key=access, secret_key=sercet);

    # function 
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

