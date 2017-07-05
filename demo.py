import time
import urllib2

from lib.client import Client, get_api_path
from formula.K import KLine
from formula.MACD import MACD
from formula.Formula import SMA
from formula.Formula import MA
from formula.Formula import EMA
from formula.Formula import HIGH
from formula.Formula import LOW
from BotConfig import BotConfig
from rule.Rule import Rule
from user.User import User
'''
out = [];
SMA([1,2,3,4,5,6],out,3,1);
print out;
out = [];
MA([1,2,3,4,5,6], out, 3);
print out;
out = [];
EMA([1,2,3,4,5,6], out, 3);
print out;
out = [];
HIGH([6,5,4,3,2,1], out, 3);
print out;
out = [];
LOW([1,2,3,4,5,6], out, 3);
print out;
def ft():
    return 1,2;
x,y = ft();
print x,y
'''
u = User();

r = Rule('btc', 240);
c = Client(access_key=BotConfig.access_key, secret_key=BotConfig.secret_key)
d = c.get(get_api_path('k'), params={'market': '{0}cny'.format("btc"), 'limit':500,'period' : '{0}'.format(240)});

print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(d[0][0]));
for k,v in enumerate(d):
	# print [v];
	r.Run([v]);
	ret = r.Do();
	if ret != None:
	    print k, "  ", ret, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(v[0])), "\n";

print r.WaveKline;
#client = Client(access_key='N1vXgZ0wSrTkLjgzG1oli4aD10DDRQW9gYxkHljW', secret_key='Xgz0QqlvdAx9lBjpiVLlnFOs2IwaPS3lftuw4geS')
"""
#demo of GET APIs

#get member info
print client.get(get_api_path('members'))

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
"""

