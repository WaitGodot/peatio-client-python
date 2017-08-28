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
from exchange.yunbi.client import Client, get_api_path
from exchange.yunbiEX import yunbiEXLocal
from Time import Time

'''
# k test
c = Client(access_key=RebotConfig.access_key, secret_key=RebotConfig.secret_key)
while True:
    time.sleep(1);
    d = c.get(get_api_path('k'), params={'market': 'eoscny', 'limit':1,'period':5});
    t = c.get(get_api_path('tickers'), params={'market':'eoscny'});
    print d, t;

'''

# 30 60 120 240 360
# btc 120, 60
# ans 60, 240
# eth 120, 360
# omg 240, 120
# zec 240, 60
# qtum 60, 240
# bts 240, 360
# gxs 240, 360
# eos 30, 60
# sc 60, 360
# snt 360, 240
# dgd 360, 240
# 1st 60, 120
# rep 60, 120
# gnt 360, 240
# etc 120, 240

r = Rebot(240);
t = 0;
while True:
    t += 1;
    # print "do", t;
    # time.sleep(0.1);
    r.run();
    # print '------------------------------------------------------------------------'
    if t > 350 * 2:
        break;

for k,v in(r.rules.items()):
    v.KDJ.Export('C:\\Users\\randy\\kdj.csv')
#    v.Export("C:\\Users\\randy\\ma.csv");
#    v.ExportWave("C:\\Users\\randy\\wave.csv")
'''
v = r.rules['anscny'];
v.Export("C:\\Users\\randy\\ma.csv");
v.ExportWave("C:\\Users\\randy\\wave.csv")
v.wavepointm3.ExportTrend(v.KLines, 'C:\\Users\\randy\\wavepointma3trend.csv');
v.wavewavepointm3.ExportTrend(v.KLines, 'C:\\Users\\randy\\wavewavepointma3trend.csv')
for k, seg in enumerate(v.wavepointm3.segs):
    print  time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(v.KLines[seg.start.idx].t)), seg;
'''
print '\n\norders'
alltradetimes = 0;
allwintimes = 0;
srotscale=[]
for k,v in enumerate(r.markets):
    market = v['id'];
    ods = r.user.getOrderMarket(market);
    if len(ods) > 0:
        buys = [];
        tradetimes = 0;
        wintimes = 0;
        print 'market:%s' % market;
        for k,v in enumerate(ods):
            if v.type == 'buy':
                tradetimes += 1;
                alltradetimes += 1;
                buys.append(v);
            if v.type == 'sell':
                print '\t',v;
                for bk, bv in enumerate(buys):
                    scale = (v.averageprice - bv.averageprice)/bv.averageprice * 100;
                    if scale > 0:
                        wintimes += 1;
                        allwintimes += 1;
                    srotscale.append([bv.ext['sort'], scale])
                    print '\t\tscale:%s, order:%s' % (scale, bv.__str__());
                buys = [];
        print '\twinner: %f, win: %d, all %d\n' % (float(wintimes)/ float(tradetimes) * 100, wintimes, tradetimes);

print 'all winner: %f, win: %d, all %d\n' % (float(allwintimes)/ float(alltradetimes) * 100, allwintimes, alltradetimes);

import csv
f = open('C:\\Users\\randy\\scales6.csv', 'wb');
w = csv.writer(f);
w.writerow(['scale']);
for k in range(0, len(r.scales)):
    w.writerow([k, r.scales[k]]);
f.close();

f = open('C:\\Users\\randy\\scalessort.csv', 'wb');
w = csv.writer(f);
w.writerow(['sort', 'scale']);
for k in range(0, len(srotscale)):
    w.writerow([srotscale[k][0], srotscale[k][1]]);
f.close();



'''
r = Rebot(); # 60, 240
t = 0;
while True:
    t+=1;
    print "do", t;
    # time.sleep(0.1);
    r.run();
    if t > 4000:
        break;
'''
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

