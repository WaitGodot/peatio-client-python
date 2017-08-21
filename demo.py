import time
import urllib2

from exchange.Exchange import Exchange
from exchange.yunbiEX import yunbiEX

from formula.K import KLine
from formula.MACD import MACD
from formula.Formula import SMA
from formula.Formula import MA
from formula.Formula import EMA
from formula.Formula import HIGH
from formula.Formula import LOW
from RebotConfig import RebotConfig
from rule.Rule import Rule
from rule.MutliMovingAverage import MutliMovingAverage
from user.User import User
from Rebot import Rebot;

r = Rebot(60);

#r.run();
t = 0;
while True:
    t+=1;
    print "do", t;
    time.sleep(1);
    r.run();

'''
market = 'ans';
u = User();
# def buy(self, market, time, price, count=None):
r = MutliMovingAverage(market, 240);
c = Client(access_key=RebotConfig.access_key, secret_key=RebotConfig.secret_key)
d = c.get(get_api_path('k'), params={'market': '{0}cny'.format(market), 'limit':500,'period':'{0}'.format(60)});

print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(d[0][0]));
for key,value in enumerate(d):
    r.Run([value]);
    ret=r.Do();
    k = r.KLines.Get(-1);

    if ret == 'buy':
        u.buy(market, k.t, k.c);
    if ret == "sell":
        u.sell(market, k.t, k.c);
    #
    count = u.positions.get(market);
    if count > 0:
        sun = -0.077;
        if (count * k.c + u.amount - u.preamount)/u.preamount < sun:
            print "sell zhi sun"
            u.sell(market, k.t, ((sun + -0.02) * u.preamount + u.preamount - u.amount)/count);

'''

#print r.WaveKline;
#client = Client(access_key='N1vXgZ0wSrTkLjgzG1oli4aD10DDRQW9gYxkHljW', secret_key='Xgz0QqlvdAx9lBjpiVLlnFOs2IwaPS3lftuw4geS')
'''
#demo of GET APIs
exchange = Exchange(RebotConfig.access_key, RebotConfig.secret_key);
exchange.delegate(yunbiEX());
u = User();
# markets
markets = exchange.getMarkets();
#get user info
# do while
info = exchange.getUser();
u.updatePositions(info['accounts']);
for key,value in enumerate(markets):
    market = value['id'];
    u.updateOrder(exchange.getOrder(market));
'''
#print '-------------------------------------------------------'
#print exchange.doOrder('snt', 'sell', '1.0', 10);
#print exchange.doOrderCancel(485916175);
#print '-------------------------------------------------------'
#print exchange.getOrder('snt');

'''
#get markets
markets =  client.get(get_api_path('markets'))
print "markets:", markets

#get tickers of each market
#market should be specified in url
print 
print "tickers in markets"
for market in markets:
    print client.get(get_api_path('tickers') % market['id'], None, False)

#get orders of each market
#market should be specified in params
print 
print "orders in markets"
for market in markets:
    print client.get(get_api_path('orders'), {'market': market['id']})

#get order book
print client.get(get_api_path('order_book'), params={'market': 'btccny'})

#get tardes
print client.get(get_api_path('trades'), params={'market': 'btccny'})

#get my trades
print client.get(get_api_path('my_trades'), params={'market': 'btccny'})
"""

#demo of POST APIs
#DANGROUS, you better use test account to debug POST APIs

"""
markets =  client.get(get_api_path('markets'))
print markets

#sell 10 dogecoins at price 0.01
params = {'market': 'dogcny', 'side': 'sell', 'volume': 10, 'price': 0.01}
res = client.post(get_api_path('orders'), params)
print res

#buy 10 dogecoins at price 0.001
params = {'market': 'dogcny', 'side': 'buy', 'volume': 10, 'price': 0.001}
res = client.post(get_api_path('orders'), params)
print res

#clear all orders in all markets
res = client.post(get_api_path('clear'))
print res
#delete a specific order by order_id

#first, let's create an sell order
#sell 10 dogecoins at price 0.01
params = {'market': 'dogcny', 'side': 'sell', 'volume': 12, 'price': 0.01}
res = client.post(get_api_path('orders'), params)
print res
order_id = res['id']

#delete this order
params = {"id": order_id}
res = client.post(get_api_path('delete_order'), params)
print res

#create multi orders
params = {'market': 'dogcny', 'orders': [{'side': 'buy', 'volume': 12, 'price': 0.0002}, {'side': 'sell', 'volume': 11, 'price': 0.01}]}
res = client.post(get_api_path('multi_orders'), params)
print res
'''

