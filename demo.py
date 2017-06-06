import time
import urllib2
import MySQLdb

from lib.client import Client, get_api_path
from formula.K import K
from formula.MACD import MACD
from formula.Formula import EMA

db = MySQLdb.connect("localhost", "randy", "randy521", "bot");
cursor = db.cursor();
cursor.execute("SELECT VERSION()");
version = cursor.fetchone();

# create table.
cursor.execute('''CREATE TABLE IF NOT EXISTS kline (
    id INT NOT NULL AUTO_INCREMENT, 
    name VARCHAR(25), 
    PRIMARY KEY (id));''');

cursor.execute('''insert into kline
	(name)
	values
	("randy1");''')
cursor.execute('''insert into kline
	(name)
	values
	("randy2");''')
cursor.execute('''insert into kline
	(name)
	values
	("randy3");''')
cursor.execute('''insert into kline
	(name)
	values
	("randy4");''')

cursor.execute('''select * from kline;''');
data = cursor.fetchall();

db.commit();

cursor.close();
db.close();
print version;
print data;
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
#get k line
macd = MACD();
d = client.get(get_api_path('k'), params={'market': 'btscny', 'limit' : '10000', 'period' : '30', 'timestamp' : '1495584000'});
KS = [];
for k, v in enumerate(d):
    print k, v
    #KS.append(K(v));
macd.Input(KS);
print macd;

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
